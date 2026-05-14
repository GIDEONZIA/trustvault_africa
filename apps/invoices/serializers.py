from rest_framework import serializers

from .models import Invoice


class InvoiceSerializer(serializers.ModelSerializer):
    balance = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)
    days_overdue = serializers.IntegerField(read_only=True)
    tenant_name = serializers.CharField(source='lease.tenant.full_name', read_only=True)
    unit_number = serializers.CharField(source='lease.unit.unit_number', read_only=True)
    property_name = serializers.CharField(source='lease.unit.building.name', read_only=True)

    class Meta:
        model = Invoice
        fields = [
            'id', 'invoice_number', 'invoice_type', 'amount', 'amount_paid',
            'balance', 'issue_date', 'due_date', 'paid_date', 'status',
            'description', 'line_items', 'days_overdue', 'reminder_count',
            'tenant_name', 'unit_number', 'property_name', 'created_at',
        ]
        read_only_fields = ['id', 'invoice_number', 'created_at']
