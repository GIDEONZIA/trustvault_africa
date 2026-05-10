from django.contrib import admin
from .models import Invoice, InvoiceItem, Receipt

class InvoiceItemInline(admin.TabularInline):
    model = InvoiceItem
    extra = 1

class ReceiptInline(admin.TabularInline):
    model = Receipt
    readonly_fields = ('receipt_number', 'amount_paid', 'payment_date', 'payment_method')
    extra = 0

@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('invoice_number', 'tenant', 'lease', 'total_amount', 'balance_due', 'status', 'due_date')
    list_filter = ('status', 'issue_date', 'due_date')
    search_fields = ('invoice_number', 'tenant__email', 'lease__unit__unit_number')
    inlines = [InvoiceItemInline, ReceiptInline]
    readonly_fields = ('balance_due',)

    def save_model(self, request, obj, form, change):
        # Auto-calculate balance before saving
        obj.balance_due = obj.total_amount - obj.amount_paid
        super().save_model(request, obj, form, change)

@admin.register(Receipt)
class ReceiptAdmin(admin.ModelAdmin):
    list_display = ('receipt_number', 'invoice', 'amount_paid', 'payment_date', 'payment_method')
    search_fields = ('receipt_number', 'invoice__invoice_number')
    readonly_fields = ('created_at',)
