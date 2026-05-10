from django.contrib import admin
from .models import Property, Unit, Amenity, PropertyImage

class UnitInline(admin.TabularInline):
    model = Unit
    extra = 1
    show_change_link = True

class AmenityInline(admin.TabularInline):
    model = Amenity
    extra = 2

class PropertyImageInline(admin.TabularInline):
    model = PropertyImage
    extra = 1

@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ('name', 'landlord', 'city', 'property_type', 'is_active')
    list_filter = ('property_type', 'city', 'is_active')
    search_fields = ('name', 'address', 'landlord__email')
    inlines = [UnitInline]

@admin.register(Unit)
class UnitAdmin(admin.ModelAdmin):
    list_display = ('unit_number', 'property', 'unit_type', 'monthly_rent', 'is_available')
    list_filter = ('unit_type', 'is_available', 'property')
    search_fields = ('unit_number', 'property__name')
    inlines = [AmenityInline, PropertyImageInline]

admin.site.register(Amenity)
admin.site.register(PropertyImage)
