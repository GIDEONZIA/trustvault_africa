from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .models import Lease

# Create your views here.
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Lease

class LeaseListView(LoginRequiredMixin, ListView):
    model = Lease
    template_name = 'tenants/lease_list.html'
    context_object_name = 'leases'

    def get_queryset(self):
        # Users only see their own leases, Staff/Superusers see all
        if self.request.user.is_staff:
            return Lease.objects.all()
        return Lease.objects.filter(tenant=self.request.user)

class LeaseDetailView(LoginRequiredMixin, DetailView):
    model = Lease
    template_name = 'tenants/lease_detail.html'
    context_object_name = 'lease'
    def get_queryset(self):
        # Users only see their own leases, Staff/Superusers see all
        if self.request.user.is_staff:
            return Lease.objects.all()
        return Lease.objects.filter(tenant=self.request.user)
    

class LeaseCreateView(LoginRequiredMixin, CreateView):
    model = Lease
    template_name = 'tenants/lease_form.html'
    fields = ['property', 'unit', 'tenant', 'start_date', 'end_date', 'monthly_rent', 'deposit_amount']
    success_url = reverse_lazy('tenants:lease_list')
