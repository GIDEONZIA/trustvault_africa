from django.contrib import admin
from .models import Lease, TenantProfile

@admin.register(Lease)
class LeaseAdmin(admin.ModelAdmin):
    # What you see in the main list
    list_display = (
        'lease_number', 
        'unit', 
        'tenant', 
        'start_date', 
        'end_date', 
        'status', 
        'monthly_rent'
    )
    
    # Sidebar filters
    list_filter = ('status', 'deposit_status', 'is_renewable', 'start_date')
    
    # Search box functionality
    search_fields = ('lease_number', 'tenant__email', 'unit__unit_number')
    
    # Organizing the detail/edit page
    fieldsets = (
        ('Identification', {
            'fields': ('lease_number', 'unit', 'tenant', 'status')
        }),
        ('Lease Terms', {
            'fields': ('start_date', 'end_date', 'monthly_rent', 'payment_day')
        }),
        ('Financial Status', {
            'fields': ('deposit_paid', 'deposit_status')
        }),
        ('Documents & Renewals', {
            'fields': ('lease_document', 'terms_accepted', 'is_renewable', 'auto_renew')
        }),
        ('Termination', {
            'fields': ('termination_date', 'termination_reason'),
            'classes': ('collapse',), # Hides this section by default
        }),
    )

    # Automatically set timestamps
    readonly_fields = ('created_at', 'updated_at')

@admin.register(TenantProfile)
class TenantProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'employer_name', 'employment_type', 'tenant_score')
    search_fields = ('user__email', 'employer_name')
