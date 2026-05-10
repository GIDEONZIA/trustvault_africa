from django.shortcuts import render

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