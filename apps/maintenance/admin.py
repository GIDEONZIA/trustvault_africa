from django.contrib import admin

from .models import MaintenanceRequest


@admin.register(MaintenanceRequest)
class MaintenanceRequestAdmin(admin.ModelAdmin):
    list_display = ('request_number', 'title', 'category', 'priority', 'status', 'tenant', 'submitted_at')
    list_filter = ('status', 'category', 'priority')
    search_fields = ('request_number', 'title', 'tenant__email')
