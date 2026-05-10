from django.db import models
from django.core.validators import MinValueValidator
from apps.core.models import TimestampedModel


class Transaction(TimestampedModel):
    TRANSACTION_TYPES = [
        ('rent', 'Rent Payment'),
        ('deposit', 'Security Deposit'),
        ('late_fee', 'Late Fee'),
        ('utility', 'Utility Payment'),
        ('maintenance', 'Maintenance Cost'),
        ('refund', 'Refund'),
    ]

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded'),
    ]

    tenant = models.ForeignKey(
        'accounts.User',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='transactions'
    )
    invoice = models.ForeignKey(
        'invoices.Invoice',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='transactions'
    )
    
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    payment_method = models.CharField(max_length=20, choices=[('mpesa', 'M-Pesa'), ('bank', 'Bank Transfer'), ('cash', 'Cash')])
    reference = models.CharField(max_length=255, blank=True)
    
    description = models.TextField(blank=True)
    processed_at = models.DateTimeField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'payments_transaction'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.transaction_type} - KES {self.amount}"


class MpesaPayment(TimestampedModel):
    transaction = models.OneToOneField(
        Transaction,
        on_delete=models.CASCADE,
        related_name='mpesa_details'
    )
    
    merchant_request_id = models.CharField(max_length=255)
    checkout_request_id = models.CharField(max_length=255, db_index=True)
    mpesa_receipt_number = models.CharField(max_length=50, blank=True, db_index=True)
    
    phone_number = models.CharField(max_length=15)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    
    result_code = models.CharField(max_length=10, blank=True)
    result_desc = models.TextField(blank=True)
    
    callback_received = models.BooleanField(default=False)
    callback_processed = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'payments_mpesa_payment'

    def __str__(self):
        return f"M-Pesa: {self.checkout_request_id}"


class PaymentSchedule(TimestampedModel):
    lease = models.ForeignKey(
        'tenants.Lease',
        on_delete=models.CASCADE,
        related_name='payment_schedules'
    )
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    due_day = models.PositiveIntegerField()
    is_active = models.BooleanField(default=True)
    last_run = models.DateTimeField(null=True, blank=True)
    next_run = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'payments_payment_schedule'

    def __str__(self):
        return f"Schedule for {self.lease} - Day {self.due_day}"
