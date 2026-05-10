from django.contrib import admin
from .models import MaintenanceRequest, Vendor, MaintenanceTask, MaintenanceExpense

class MaintenanceExpenseInline(admin.TabularInline):
    model = MaintenanceExpense
    extra = 1

class MaintenanceTaskInline(admin.StackedInline):
    model = MaintenanceTask
    extra = 0
    show_change_link = True

@admin.register(MaintenanceRequest)
class MaintenanceRequestAdmin(admin.ModelAdmin):
    list_display = ('unit', 'category', 'priority', 'status', 'tenant', 'created_at')
    list_filter = ('status', 'priority', 'category')
    search_fields = ('unit__unit_number', 'description', 'tenant__email')
    inlines = [MaintenanceTaskInline]

@admin.register(Vendor)
class VendorAdmin(admin.ModelAdmin):
    list_display = ('name', 'specialty', 'phone', 'rating', 'is_active')
    list_filter = ('specialty', 'is_active')
    search_fields = ('name', 'phone')

@admin.register(MaintenanceTask)
class MaintenanceTaskAdmin(admin.ModelAdmin):
    list_display = ('request', 'vendor', 'status', 'estimated_cost', 'actual_cost', 'scheduled_date')
    list_filter = ('status', 'scheduled_date')
    inlines = [MaintenanceExpenseInline]

admin.site.register(MaintenanceExpense)
