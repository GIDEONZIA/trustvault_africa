from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import CreateView, DetailView, ListView, UpdateView

from .forms import PropertyForm, UnitForm
from .models import Property, Unit


class PropertyListView(LoginRequiredMixin, ListView):
    model = Property
    template_name = 'properties/property_list.html'
    context_object_name = 'properties'
    paginate_by = 10

    def get_queryset(self):
        return Property.objects.filter(owner=self.request.user, is_active=True).prefetch_related('units')


class PropertyDetailView(LoginRequiredMixin, DetailView):
    model = Property
    template_name = 'properties/property_detail.html'
    context_object_name = 'property'

    def get_queryset(self):
        return Property.objects.filter(owner=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['units'] = self.object.units.all()
        return context


class PropertyCreateView(LoginRequiredMixin, CreateView):
    model = Property
    form_class = PropertyForm
    template_name = 'properties/property_form.html'

    def form_valid(self, form):
        form.instance.owner = self.request.user
        messages.success(self.request, 'Property created successfully.')
        return super().form_valid(form)


class PropertyUpdateView(LoginRequiredMixin, UpdateView):
    model = Property
    form_class = PropertyForm
    template_name = 'properties/property_form.html'

    def get_queryset(self):
        return Property.objects.filter(owner=self.request.user)

    def form_valid(self, form):
        messages.success(self.request, 'Property updated successfully.')
        return super().form_valid(form)


@login_required
def property_delete(request, slug):
    prop = get_object_or_404(Property, slug=slug, owner=request.user)
    if request.method == 'POST':
        prop.is_active = False
        prop.save()
        messages.success(request, 'Property deactivated.')
        return redirect('properties:list')
    return render(request, 'properties/property_confirm_delete.html', {'property': prop})


@login_required
def unit_create(request, property_slug):
    prop = get_object_or_404(Property, slug=property_slug, owner=request.user)
    if request.method == 'POST':
        form = UnitForm(request.POST)
        if form.is_valid():
            unit = form.save(commit=False)
            unit.building = prop
            unit.save()
            messages.success(request, f'Unit {unit.unit_number} added.')
            return redirect('properties:detail', slug=prop.slug)
    else:
        form = UnitForm()
    return render(request, 'properties/unit_form.html', {'form': form, 'property': prop})


@login_required
def unit_update(request, pk):
    unit = get_object_or_404(Unit, pk=pk, building__owner=request.user)
    if request.method == 'POST':
        form = UnitForm(request.POST, instance=unit)
        if form.is_valid():
            form.save()
            messages.success(request, f'Unit {unit.unit_number} updated.')
            return redirect('properties:detail', slug=unit.building.slug)
    else:
        form = UnitForm(instance=unit)
    return render(request, 'properties/unit_form.html', {'form': form, 'property': unit.building, 'unit': unit})


@login_required
def unit_delete(request, pk):
    unit = get_object_or_404(Unit, pk=pk, building__owner=request.user)
    if request.method == 'POST':
        prop_slug = unit.building.slug
        unit.delete()
        messages.success(request, 'Unit deleted.')
        return redirect('properties:detail', slug=prop_slug)
    return render(request, 'properties/unit_confirm_delete.html', {'unit': unit})
