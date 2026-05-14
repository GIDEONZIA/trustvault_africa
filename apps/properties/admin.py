from django.contrib import admin

from .models import Property, Unit


class UnitInline(admin.TabularInline):
    model = Unit
    extra = 0


@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'city', 'property_type', 'is_active', 'is_listed')
    list_filter = ('property_type', 'city', 'is_active', 'is_listed')
    search_fields = ('name', 'address', 'city')
    prepopulated_fields = {'slug': ('name',)}
    inlines = [UnitInline]


@admin.register(Unit)
class UnitAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'unit_type', 'monthly_rent', 'is_available', 'is_published')
    list_filter = ('unit_type', 'is_available', 'is_published')
    search_fields = ('unit_number', 'building__name')
