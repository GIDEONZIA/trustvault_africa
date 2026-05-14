from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import DetailView, ListView

from .forms import InvoiceForm
from .models import Invoice


class InvoiceListView(LoginRequiredMixin, ListView):
    model = Invoice
    template_name = 'invoices/invoice_list.html'
    context_object_name = 'invoices'
    paginate_by = 20

    def get_queryset(self):
        user = self.request.user
        qs = Invoice.objects.select_related('lease', 'lease__tenant', 'lease__unit', 'lease__unit__building')
        if user.is_landlord:
            qs = qs.filter(lease__unit__building__owner=user)
        else:
            qs = qs.filter(lease__tenant=user)

        status_filter = self.request.GET.get('status')
        if status_filter:
            qs = qs.filter(status=status_filter)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        qs = self.get_queryset()
        from django.db.models import Sum
        context['total_outstanding'] = qs.filter(
            status__in=['pending', 'partially_paid', 'overdue']
        ).aggregate(total=Sum('amount') - Sum('amount_paid'))['total'] or 0
        return context


class InvoiceDetailView(LoginRequiredMixin, DetailView):
    model = Invoice
    template_name = 'invoices/invoice_detail.html'
    context_object_name = 'invoice'

    def get_queryset(self):
        user = self.request.user
        if user.is_landlord:
            return Invoice.objects.filter(lease__unit__building__owner=user)
        return Invoice.objects.filter(lease__tenant=user)


@login_required
def invoice_create(request):
    if request.method == 'POST':
        form = InvoiceForm(request.POST)
        if form.is_valid():
            invoice = form.save()
            messages.success(request, f'Invoice {invoice.invoice_number} created.')
            return redirect('invoices:detail', pk=invoice.pk)
    else:
        form = InvoiceForm()
    return render(request, 'invoices/invoice_form.html', {'form': form})


@login_required
def invoice_send_reminder(request, pk):
    invoice = get_object_or_404(Invoice, pk=pk, lease__unit__building__owner=request.user)
    invoice.reminder_count += 1
    invoice.save()
    messages.success(request, 'Payment reminder sent.')
    return redirect('invoices:detail', pk=invoice.pk)


@login_required
def invoice_waive(request, pk):
    invoice = get_object_or_404(Invoice, pk=pk, lease__unit__building__owner=request.user)
    if request.method == 'POST':
        invoice.status = 'waived'
        invoice.save()
        messages.success(request, f'Invoice {invoice.invoice_number} waived.')
        return redirect('invoices:list')
    return render(request, 'invoices/invoice_waive.html', {'invoice': invoice})
