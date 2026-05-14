from rest_framework import serializers

from .models import Payment, Receipt


class ReceiptSerializer(serializers.ModelSerializer):
    class Meta:
        model = Receipt
        fields = ['receipt_number', 'amount', 'payment_date', 'pdf_url']


class PaymentSerializer(serializers.ModelSerializer):
    receipt = ReceiptSerializer(read_only=True)

    class Meta:
        model = Payment
        fields = [
            'id', 'amount', 'payment_method', 'transaction_id',
            'mpesa_receipt', 'phone_number', 'status', 'processed_at',
            'failure_reason', 'receipt', 'created_at',
        ]
        read_only_fields = ['id', 'created_at']


class PaymentInitiateSerializer(serializers.Serializer):
    invoice_id = serializers.IntegerField()
    phone_number = serializers.CharField(max_length=15)
    amount = serializers.DecimalField(max_digits=12, decimal_places=2)
