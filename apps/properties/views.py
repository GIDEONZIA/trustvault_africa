from django.shortcuts import render

# Create your views here.
from django.views.generic import ListView, DetailView
from .models import Property, Unit

class PropertyListView(ListView):
    model = Property
    template_name = 'properties/property_list.html'
    context_object_name = 'properties'
    
    def get_queryset(self):
        return Property.objects.filter(is_active=True)

class PropertyDetailView(DetailView):
    model = Property
    template_name = 'properties/property_detail.html'
    context_object_name = 'property'

class UnitDetailView(DetailView):
    model = Unit
    template_name = 'properties/unit_detail.html'
    context_object_name = 'unit'
