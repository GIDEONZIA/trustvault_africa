from django.contrib import admin

from .models import Payment, Receipt


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('transaction_id', 'tenant', 'amount', 'payment_method', 'status', 'created_at')
    list_filter = ('status', 'payment_method')
    search_fields = ('transaction_id', 'mpesa_receipt', 'tenant__email')


@admin.register(Receipt)
class ReceiptAdmin(admin.ModelAdmin):
    list_display = ('receipt_number', 'tenant_name', 'amount', 'payment_date')
    search_fields = ('receipt_number', 'tenant_name')
