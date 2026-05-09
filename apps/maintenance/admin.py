from django.contrib import admin
from .models import MaintenanceRequest

@admin.register(MaintenanceRequest)
class MaintenanceRequestAdmin(admin.ModelAdmin):
    list_display = ('request_number', 'unit', 'category', 'priority', 'status', 'submitted_at')
    list_filter = ('status', 'priority', 'category')
    search_fields = ('request_number', 'title', 'unit__unit_number')
    readonly_fields = ('submitted_at', 'updated_at')
