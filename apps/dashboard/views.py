from django.shortcuts import render

# Create your views here.
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from apps.properties.models import Unit
from apps.tenants.models import Lease
from apps.payments.models import Transaction
from django.db.models import Sum

class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Aggregate stats for the Landlord/Admin
        context['total_units'] = Unit.objects.count()
        context['vacant_units'] = Unit.objects.filter(is_available=True).count()
        context['active_leases'] = Lease.objects.filter(status='active').count()
        
        # Financial Summary
        total_collected = Transaction.objects.filter(
            status='completed'
        ).aggregate(Sum('amount'))['amount__sum'] or 0
        context['revenue'] = total_collected

        return context
