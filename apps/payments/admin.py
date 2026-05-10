from django.contrib import admin
from .models import Transaction, MpesaPayment, PaymentSchedule

class MpesaPaymentInline(admin.StackedInline):
    model = MpesaPayment
    readonly_fields = ('merchant_request_id', 'checkout_request_id', 'mpesa_receipt_number', 'amount')
    extra = 0

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('reference', 'tenant', 'amount', 'transaction_type', 'status', 'payment_method', 'created_at')
    list_filter = ('status', 'transaction_type', 'payment_method', 'created_at')
    search_fields = ('reference', 'tenant__email', 'description')
    inlines = [MpesaPaymentInline]
    date_hierarchy = 'created_at'

@admin.register(MpesaPayment)
class MpesaPaymentAdmin(admin.ModelAdmin):
    list_display = ('mpesa_receipt_number', 'phone_number', 'amount', 'result_code', 'callback_received')
    list_filter = ('callback_received', 'result_code')
    search_fields = ('mpesa_receipt_number', 'checkout_request_id', 'phone_number')
    readonly_fields = ('created_at',)

@admin.register(PaymentSchedule)
class PaymentScheduleAdmin(admin.ModelAdmin):
    list_display = ('lease', 'amount', 'due_day', 'is_active', 'next_run')
    list_filter = ('is_active', 'due_day')
