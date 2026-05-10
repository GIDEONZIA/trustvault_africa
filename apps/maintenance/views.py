from django.shortcuts import render

# Create your views here.
from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import MaintenanceRequest

class MaintenanceRequestListView(LoginRequiredMixin, ListView):
    model = MaintenanceRequest
    template_name = 'maintenance/request_list.html'
    context_object_name = 'requests'

    def get_queryset(self):
        if self.request.user.is_staff:
            return MaintenanceRequest.objects.all()
        return MaintenanceRequest.objects.filter(tenant=self.request.user)

class MaintenanceRequestDetailView(LoginRequiredMixin, DetailView):
    model = MaintenanceRequest
    template_name = 'maintenance/request_detail.html'

class MaintenanceRequestCreateView(LoginRequiredMixin, CreateView):
    model = MaintenanceRequest
    fields = ['unit', 'category', 'description', 'priority', 'preferred_date', 'preferred_time', 'photo_1']
    template_name = 'maintenance/request_form.html'
    success_url = reverse_lazy('maintenance:request_list')

    def form_valid(self, form):
        form.instance.tenant = self.request.user
        return super().form_valid(form)
