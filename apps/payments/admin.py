from django.contrib import admin
from .models import Payment

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('mpesa_receipt', 'invoice', 'tenant', 'amount', 'status', 'created_at')
    list_filter = ('status', 'payment_method', 'created_at')
    search_fields = ('mpesa_receipt', 'checkout_request_id', 'tenant__email')
    readonly_fields = ('raw_response', 'processed_at')
