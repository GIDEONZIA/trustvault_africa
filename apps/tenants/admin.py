from django.contrib import admin
from .models import Lease, LeaseDocument, TenantUnit, MoveInChecklist

class LeaseDocumentInline(admin.TabularInline):
    model = LeaseDocument
    extra = 1

class MoveInChecklistInline(admin.TabularInline):
    model = MoveInChecklist
    extra = 3

@admin.register(Lease)
class LeaseAdmin(admin.ModelAdmin):
    list_display = ('tenant', 'unit', 'status', 'start_date', 'end_date', 'monthly_rent')
    list_filter = ('status', 'auto_renew', 'start_date')
    search_fields = ('tenant__email', 'unit__unit_number')
    inlines = [LeaseDocumentInline]
    actions = ['mark_as_active']

    @admin.action(description="Mark selected leases as Active")
    def mark_as_active(self, request, queryset):
        queryset.update(status='active')

@admin.register(TenantUnit)
class TenantUnitAdmin(admin.ModelAdmin):
    list_display = ('tenant', 'unit', 'move_in_date', 'is_active')
    list_filter = ('is_active',)
    inlines = [MoveInChecklistInline]

admin.site.register(LeaseDocument)
admin.site.register(MoveInChecklist)
