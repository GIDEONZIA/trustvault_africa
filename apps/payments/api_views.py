import json
import logging
import uuid

from django.utils import timezone
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.invoices.models import Invoice

from .models import Payment, Receipt
from .mpesa import mpesa_service
from .serializers import PaymentInitiateSerializer, PaymentSerializer

logger = logging.getLogger(__name__)


class PaymentInitiateAPIView(APIView):
    def post(self, request):
        serializer = PaymentInitiateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        try:
            invoice = Invoice.objects.get(pk=data['invoice_id'])
        except Invoice.DoesNotExist:
            return Response({'success': False, 'message': 'Invoice not found'}, status=404)

        phone = data['phone_number'].replace('+', '').replace(' ', '')
        amount = data['amount']

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
            return Response({
                'success': True,
                'data': {
                    'checkout_request_id': result['checkout_request_id'],
                    'merchant_request_id': result['merchant_request_id'],
                    'status': 'pending',
                    'message': result.get('message', 'STK push sent'),
                },
                'message': 'Payment initiated',
            }, status=status.HTTP_202_ACCEPTED)

        payment.status = 'failed'
        payment.failure_reason = result.get('error', '')
        payment.save()
        return Response({
            'success': False,
            'message': result.get('error', 'Payment failed'),
        }, status=status.HTTP_400_BAD_REQUEST)


class MpesaCallbackAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        try:
            callback_data = json.loads(request.body) if isinstance(request.body, bytes) else request.data
            result = mpesa_service.process_callback(callback_data)

            checkout_id = result.get('checkout_request_id')
            if not checkout_id:
                return Response({'ResultCode': 1, 'ResultDesc': 'Missing checkout ID'})

            try:
                payment = Payment.objects.get(checkout_request_id=checkout_id)
            except Payment.DoesNotExist:
                return Response({'ResultCode': 0, 'ResultDesc': 'Accepted'})

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
                payment.failure_reason = result.get('result_desc', '')
                payment.save()

            return Response({'ResultCode': 0, 'ResultDesc': 'Accepted'})
        except Exception as e:
            logger.error(f'Callback error: {e}')
            return Response({'ResultCode': 1, 'ResultDesc': 'Error'})


class PaymentStatusAPIView(APIView):
    def get(self, request, pk):
        try:
            payment = Payment.objects.select_related('receipt').get(pk=pk)
        except Payment.DoesNotExist:
            return Response({'success': False, 'message': 'Not found'}, status=404)

        return Response({
            'success': True,
            'data': PaymentSerializer(payment).data,
        })


class PaymentListAPIView(generics.ListAPIView):
    serializer_class = PaymentSerializer
    filterset_fields = ['status', 'payment_method']

    def get_queryset(self):
        user = self.request.user
        if user.is_landlord:
            return Payment.objects.filter(
                invoice__lease__unit__building__owner=user
            ).select_related('invoice', 'tenant', 'receipt')
        return Payment.objects.filter(tenant=user).select_related('invoice', 'receipt')
