from django.contrib import admin

from .models import Invoice, InvoiceReminder


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('invoice_number', 'lease', 'invoice_type', 'amount', 'amount_paid', 'status', 'due_date')
    list_filter = ('status', 'invoice_type', 'due_date')
    search_fields = ('invoice_number', 'lease__tenant__email')


@admin.register(InvoiceReminder)
class InvoiceReminderAdmin(admin.ModelAdmin):
    list_display = ('invoice', 'channel', 'status', 'sent_at')
