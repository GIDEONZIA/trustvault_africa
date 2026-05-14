from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import DetailView, ListView

from apps.invoices.models import Invoice
from apps.maintenance.models import MaintenanceRequest

from .forms import LeaseForm
from .models import Lease


class LeaseListView(LoginRequiredMixin, ListView):
    model = Lease
    template_name = 'tenants/lease_list.html'
    context_object_name = 'leases'
    paginate_by = 10

    def get_queryset(self):
        user = self.request.user
        if user.is_landlord:
            return Lease.objects.filter(
                unit__building__owner=user
            ).select_related('unit', 'unit__building', 'tenant')
        return Lease.objects.filter(tenant=user).select_related('unit', 'unit__building')


class LeaseDetailView(LoginRequiredMixin, DetailView):
    model = Lease
    template_name = 'tenants/lease_detail.html'
    context_object_name = 'lease'

    def get_queryset(self):
        user = self.request.user
        if user.is_landlord:
            return Lease.objects.filter(unit__building__owner=user)
        return Lease.objects.filter(tenant=user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['invoices'] = Invoice.objects.filter(lease=self.object).order_by('-due_date')[:10]
        return context


@login_required
def lease_create(request):
    if request.method == 'POST':
        form = LeaseForm(request.POST, request.FILES)
        if form.is_valid():
            lease = form.save()
            messages.success(request, f'Lease {lease.lease_number} created.')
            return redirect('tenants:lease-detail', pk=lease.pk)
    else:
        form = LeaseForm()
        form.fields['unit'].queryset = request.user.properties.first().units.filter(is_available=True) if request.user.properties.exists() else form.fields['unit'].queryset.none()
    return render(request, 'tenants/lease_form.html', {'form': form})


@login_required
def lease_terminate(request, pk):
    lease = get_object_or_404(Lease, pk=pk, unit__building__owner=request.user, status='active')
    if request.method == 'POST':
        lease.status = 'terminated'
        lease.termination_reason = request.POST.get('reason', '')
        lease.save()
        lease.unit.is_available = True
        lease.unit.save()
        messages.success(request, f'Lease {lease.lease_number} terminated.')
        return redirect('tenants:lease-list')
    return render(request, 'tenants/lease_terminate.html', {'lease': lease})


@login_required
def tenant_portal(request):
    if not request.user.is_tenant:
        return redirect('dashboard:index')
    active_lease = Lease.objects.filter(tenant=request.user, status='active').select_related('unit', 'unit__building').first()
    pending_invoices = Invoice.objects.filter(lease__tenant=request.user, status__in=['pending', 'overdue']).order_by('due_date')
    maintenance_requests = MaintenanceRequest.objects.filter(tenant=request.user).order_by('-created_at')[:5]
    return render(request, 'tenants/portal.html', {
        'lease': active_lease,
        'pending_invoices': pending_invoices,
        'maintenance_requests': maintenance_requests,
    })
