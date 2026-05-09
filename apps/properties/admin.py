from django.contrib import admin
from .models import Property, Unit

class UnitInline(admin.TabularInline):
    model = Unit
    extra = 1  # How many empty rows to show by default

@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'city', 'property_type', 'is_active', 'total_units_count')
    list_filter = ('property_type', 'is_active', 'city')
    search_fields = ('name', 'address', 'city')
    prepopulated_fields = {'slug': ('name',)}
    inlines = [UnitInline]

@admin.register(Unit)
class UnitAdmin(admin.ModelAdmin):
    list_display = ('unit_number', 'property', 'unit_type', 'monthly_rent', 'is_available')
    list_filter = ('unit_type', 'is_available')
    search_fields = ('unit_number', 'property__name')