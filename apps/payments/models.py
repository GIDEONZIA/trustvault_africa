from django.db import models
from django.conf import settings
from apps.invoices.models import Invoice

class Payment(models.Model):
    PAYMENT_METHODS = [
        ('mpesa', 'M-Pesa'),
        ('bank_transfer', 'Bank Transfer'),
        ('cash', 'Cash'),
        ('cheque', 'Cheque'),
        ('card', 'Card'),
    ]

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded'),
    ]

    invoice = models.ForeignKey(Invoice, on_delete=models.RESTRICT, related_name='payments')
    tenant = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.RESTRICT, 
        related_name='payments'
    )

    # Payment Details
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    payment_method = models.CharField(max_length=50, choices=PAYMENT_METHODS)

    # M-Pesa Specific
    transaction_id = models.CharField(max_length=100, unique=True, blank=True, null=True)
    mpesa_receipt = models.CharField(max_length=100, blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    checkout_request_id = models.CharField(max_length=100, blank=True, null=True)
    merchant_request_id = models.CharField(max_length=100, blank=True, null=True)

    # Status
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    processed_at = models.DateTimeField(null=True, blank=True)
    failure_reason = models.TextField(blank=True, null=True)

    # Metadata
    raw_response = models.JSONField(default=dict, blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['invoice']),
            models.Index(fields=['tenant']),
            models.Index(fields=['status']),
        ]

    def __str__(self):
        return f"{self.mpesa_receipt or self.id} - {self.amount} KES"
