from django.contrib import admin
from .models import Invoice, Receipt

@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('invoice_number', 'lease', 'invoice_type', 'amount', 'balance', 'status', 'due_date')
    list_filter = ('status', 'invoice_type', 'due_date')
    search_fields = ('invoice_number', 'lease__tenant__email', 'lease__lease_number')
    readonly_fields = ('created_at', 'updated_at')

@admin.register(Receipt)
class ReceiptAdmin(admin.ModelAdmin):
    list_display = ('receipt_number', 'tenant_name', 'amount', 'payment_date', 'email_sent')
    list_filter = ('email_sent', 'sms_sent', 'payment_date')
    search_fields = ('receipt_number', 'tenant_name', 'invoice_number')
    readonly_fields = ('generated_at',)
