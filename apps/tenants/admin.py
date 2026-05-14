from django.contrib import admin

from .models import Lease, TenantProfile


@admin.register(Lease)
class LeaseAdmin(admin.ModelAdmin):
    list_display = ('lease_number', 'tenant', 'unit', 'monthly_rent', 'status', 'start_date', 'end_date')
    list_filter = ('status', 'start_date')
    search_fields = ('lease_number', 'tenant__email', 'tenant__first_name')


@admin.register(TenantProfile)
class TenantProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'employer_name', 'tenant_score')
    search_fields = ('user__email', 'user__first_name')
