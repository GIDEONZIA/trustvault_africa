import json
import logging
import uuid

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from apps.invoices.models import Invoice

from .models import Payment, Receipt
from .mpesa import mpesa_service

logger = logging.getLogger(__name__)


@login_required
def payment_initiate(request, invoice_id):
    invoice = get_object_or_404(Invoice, pk=invoice_id)
    if request.method == 'POST':
        phone = request.POST.get('phone_number', '').replace('+', '').replace(' ', '')
        amount = invoice.balance

        if not phone:
            messages.error(request, 'Phone number is required.')
            return redirect('invoices:detail', pk=invoice_id)

        payment = Payment.objects.create(
            invoice=invoice,
            tenant=request.user,
            amount=amount,
            payment_method='mpesa',
            phone_number=phone,
            transaction_id=str(uuid.uuid4()),
            status='pending',
        )

        result = mpesa_service.stk_push(
            phone_number=phone,
            amount=amount,
            account_reference=invoice.invoice_number,
            description=f'Rent payment for {invoice.description}',
        )

        if result['success']:
            payment.checkout_request_id = result['checkout_request_id']
            payment.merchant_request_id = result['merchant_request_id']
            payment.status = 'processing'
            payment.save()
            invoice.mpesa_checkout_request_id = result['checkout_request_id']
            invoice.save()
            messages.success(request, 'Payment initiated. Check your phone for the M-Pesa prompt.')
        else:
            payment.status = 'failed'
            payment.failure_reason = result.get('error', 'Unknown error')
            payment.save()
            messages.error(request, f'Payment failed: {result.get("error")}')

        return redirect('invoices:detail', pk=invoice_id)

    return render(request, 'payments/initiate.html', {'invoice': invoice})


@csrf_exempt
@require_POST
def mpesa_callback(request):
    try:
        callback_data = json.loads(request.body)
        result = mpesa_service.process_callback(callback_data)

        checkout_id = result.get('checkout_request_id')
        if not checkout_id:
            return JsonResponse({'ResultCode': 1, 'ResultDesc': 'Missing checkout ID'})

        try:
            payment = Payment.objects.get(checkout_request_id=checkout_id)
        except Payment.DoesNotExist:
            logger.error(f'Payment not found for checkout ID: {checkout_id}')
            return JsonResponse({'ResultCode': 0, 'ResultDesc': 'Accepted'})

        payment.raw_response = callback_data

        if result['success']:
            payment.status = 'completed'
            payment.mpesa_receipt = result.get('mpesa_receipt', '')
            payment.processed_at = timezone.now()
            payment.save()

            payment.invoice.record_payment(payment.amount)

            Receipt.objects.create(
                payment=payment,
                amount=payment.amount,
                payment_date=timezone.now(),
                tenant_name=payment.tenant.full_name,
                property_name=payment.invoice.lease.unit.building.name,
                unit_number=payment.invoice.lease.unit.unit_number,
                invoice_number=payment.invoice.invoice_number,
            )
        else:
            payment.status = 'failed'
            payment.failure_reason = result.get('result_desc', 'Transaction failed')
            payment.save()

        return JsonResponse({'ResultCode': 0, 'ResultDesc': 'Accepted'})

    except Exception as e:
        logger.error(f'M-Pesa callback error: {e}')
        return JsonResponse({'ResultCode': 1, 'ResultDesc': 'Error processing callback'})


@login_required
def payment_status(request, pk):
    payment = get_object_or_404(Payment, pk=pk)
    return JsonResponse({
        'success': True,
        'data': {
            'id': payment.pk,
            'status': payment.status,
            'amount': str(payment.amount),
            'mpesa_receipt': payment.mpesa_receipt,
            'processed_at': str(payment.processed_at) if payment.processed_at else None,
        },
    })


@login_required
def payment_history(request):
    user = request.user
    if user.is_landlord:
        payments = Payment.objects.filter(
            invoice__lease__unit__building__owner=user
        ).select_related('invoice', 'tenant').order_by('-created_at')
    else:
        payments = Payment.objects.filter(tenant=user).select_related('invoice').order_by('-created_at')
    return render(request, 'payments/history.html', {'payments': payments})


@login_required
def record_manual_payment(request, invoice_id):
    invoice = get_object_or_404(Invoice, pk=invoice_id, lease__unit__building__owner=request.user)
    if request.method == 'POST':
        amount = request.POST.get('amount')
        method = request.POST.get('payment_method', 'cash')
        try:
            amount = float(amount)
        except (TypeError, ValueError):
            messages.error(request, 'Invalid amount.')
            return redirect('invoices:detail', pk=invoice_id)

        payment = Payment.objects.create(
            invoice=invoice,
            tenant=invoice.lease.tenant,
            amount=amount,
            payment_method=method,
            transaction_id=str(uuid.uuid4()),
            status='completed',
            processed_at=timezone.now(),
        )
        invoice.record_payment(payment.amount)

        Receipt.objects.create(
            payment=payment,
            amount=payment.amount,
            payment_date=timezone.now(),
            tenant_name=invoice.lease.tenant.full_name,
            property_name=invoice.lease.unit.building.name,
            unit_number=invoice.lease.unit.unit_number,
            invoice_number=invoice.invoice_number,
        )

        messages.success(request, f'Payment of KES {amount:,.2f} recorded.')
        return redirect('invoices:detail', pk=invoice_id)
    return render(request, 'payments/record_manual.html', {'invoice': invoice})
