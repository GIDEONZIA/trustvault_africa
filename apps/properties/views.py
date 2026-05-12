from django.views.generic import ListView, DetailView, CreateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Property, Unit

# matches name='property_list'
class PropertyListView(LoginRequiredMixin, ListView):
    model = Property
    template_name = 'properties/property_list.html'
    context_object_name = 'properties'

# matches name='property_form'
class PropertyCreateView(LoginRequiredMixin, CreateView):
    model = Property
    template_name = 'properties/property_form.html'
    fields = ['name', 'address', 'city', 'county', 'property_type', 'description']
    success_url = reverse_lazy('properties:property_list')

    def form_valid(self, form):
        form.instance.landlord = self.request.user
        return super().form_valid(form)

# matches name='property_detail'
class PropertyDetailView(LoginRequiredMixin, DetailView):
    model = Property
    template_name = 'properties/property_detail.html'

# matches name='unit_list'
class UnitListView(LoginRequiredMixin, ListView):
    model = Unit
    template_name = 'properties/unit_list.html'
    context_object_name = 'units'

# matches name='unit_form'
class UnitCreateView(LoginRequiredMixin, CreateView):
    model = Unit
    template_name = 'properties/unit_form.html'
    fields = ['property', 'unit_number', 'unit_type', 'monthly_rent', 'is_available']
    success_url = reverse_lazy('properties:unit_list')

# matches name='unit_detail'
class UnitDetailView(LoginRequiredMixin, DetailView):
    model = Unit
    template_name = 'properties/unit_detail.html'
