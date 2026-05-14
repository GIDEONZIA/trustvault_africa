from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.generic import DetailView, ListView

from .forms import MaintenanceRequestForm, MaintenanceUpdateForm
from .models import MaintenanceRequest


class MaintenanceListView(LoginRequiredMixin, ListView):
    model = MaintenanceRequest
    template_name = 'maintenance/request_list.html'
    context_object_name = 'requests'
    paginate_by = 10

    def get_queryset(self):
        user = self.request.user
        if user.is_landlord:
            qs = MaintenanceRequest.objects.filter(
                unit__building__owner=user
            ).select_related('unit', 'unit__building', 'tenant', 'assigned_to')
        else:
            qs = MaintenanceRequest.objects.filter(tenant=user).select_related('unit', 'unit__building')

        status_filter = self.request.GET.get('status')
        if status_filter:
            qs = qs.filter(status=status_filter)
        return qs


class MaintenanceDetailView(LoginRequiredMixin, DetailView):
    model = MaintenanceRequest
    template_name = 'maintenance/request_detail.html'
    context_object_name = 'request'

    def get_queryset(self):
        user = self.request.user
        if user.is_landlord:
            return MaintenanceRequest.objects.filter(unit__building__owner=user)
        return MaintenanceRequest.objects.filter(tenant=user)


@login_required
def maintenance_create(request):
    if request.method == 'POST':
        form = MaintenanceRequestForm(request.POST)
        if form.is_valid():
            mr = form.save(commit=False)
            mr.tenant = request.user
            active_lease = request.user.leases.filter(status='active').first()
            if active_lease:
                mr.unit = active_lease.unit
            mr.save()
            messages.success(request, f'Request {mr.request_number} submitted.')
            return redirect('maintenance:detail', pk=mr.pk)
    else:
        form = MaintenanceRequestForm()
    return render(request, 'maintenance/request_form.html', {'form': form})


@login_required
def maintenance_update(request, pk):
    mr = get_object_or_404(MaintenanceRequest, pk=pk, unit__building__owner=request.user)
    if request.method == 'POST':
        form = MaintenanceUpdateForm(request.POST, instance=mr)
        if form.is_valid():
            mr = form.save(commit=False)
            if mr.status == 'under_review' and not mr.reviewed_at:
                mr.reviewed_at = timezone.now()
            if mr.status == 'in_progress' and not mr.started_at:
                mr.started_at = timezone.now()
            if mr.status == 'completed' and not mr.completed_at:
                mr.completed_at = timezone.now()
            mr.save()
            messages.success(request, 'Request updated.')
            return redirect('maintenance:detail', pk=mr.pk)
    else:
        form = MaintenanceUpdateForm(instance=mr)
    return render(request, 'maintenance/request_update.html', {'form': form, 'maintenance_request': mr})


@login_required
def maintenance_feedback(request, pk):
    mr = get_object_or_404(MaintenanceRequest, pk=pk, tenant=request.user, status='completed')
    if request.method == 'POST':
        mr.tenant_rating = int(request.POST.get('rating', 5))
        mr.tenant_feedback = request.POST.get('feedback', '')
        mr.save()
        messages.success(request, 'Feedback submitted.')
        return redirect('maintenance:detail', pk=mr.pk)
    return render(request, 'maintenance/feedback.html', {'maintenance_request': mr})
