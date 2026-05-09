from django.db import models
from django.core.validators import MinValueValidator
from apps.core.models import TimestampedModel


class Invoice(TimestampedModel):
    """
    Monthly rent invoice for a lease.
    """
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('sent', 'Sent'),
        ('partial', 'Partially Paid'),
        ('paid', 'Paid'),
        ('overdue', 'Overdue'),
        ('cancelled', 'Cancelled'),
    ]

    SEND_METHODS = [
        ('sms', 'SMS'),
        ('email', 'Email'),
        ('both', 'Both'),
    ]

    lease = models.ForeignKey(
        'tenants.Lease',
        on_delete=models.CASCADE,
        related_name='invoices'
    )
    tenant = models.ForeignKey(
        'accounts.User',
        on_delete=models.CASCADE,
        related_name='invoices'
    )
    
    # Invoice details
    invoice_number = models.CharField(max_length=50, unique=True, db_index=True)
    issue_date = models.DateField()
    due_date = models.DateField()
    
    # Amounts
    total_amount = models.DecimalField(
        max_digits=12, 
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    amount_paid = models.DecimalField(
        max_digits=12, 
        decimal_places=2, 
        default=0
    )
    balance_due = models.DecimalField(
        max_digits=12, 
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    
    # Status
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='draft'
    )
    
    # Delivery
    sent_via = models.CharField(
        max_length=20, 
        choices=SEND_METHODS,
        default='sms'
    )
    sent_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'invoices_invoice'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.invoice_number} - {self.lease.unit}"

    def save(self, *args, **kwargs):
        # Auto-calculate balance due
        self.balance_due = self.total_amount - self.amount_paid
        super().save(*args, **kwargs)


class InvoiceItem(TimestampedModel):
    """
    Line items within an invoice.
    """
    ITEM_TYPES = [
        ('rent', 'Rent'),
        ('deposit', 'Security Deposit'),
        ('utility', 'Utility'),
        ('late_fee', 'Late Fee'),
        ('other', 'Other'),
    ]

    invoice = models.ForeignKey(
        Invoice,
        on_delete=models.CASCADE,
        related_name='items'
    )
    description = models.CharField(max_length=255)
    amount = models.DecimalField(
        max_digits=12, 
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    item_type = models.CharField(
        max_length=20, 
        choices=ITEM_TYPES,
        default='rent'
    )

    class Meta:
        db_table = 'invoices_invoice_item'

    def __str__(self):
        return f"{self.description} - KES {self.amount}"


class Receipt(TimestampedModel):
    """
    Payment confirmation receipt.
    """
    invoice = models.ForeignKey(
        Invoice,
        on_delete=models.CASCADE,
        related_name='receipts'
    )
    transaction = models.ForeignKey(
        'payments.Transaction',
        on_delete=models.CASCADE,
        related_name='receipts'
    )
    amount_paid = models.DecimalField(
        max_digits=12, 
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    payment_date = models.DateTimeField()
    payment_method = models.CharField(max_length=20)
    receipt_number = models.CharField(max_length=50, unique=True)
    pdf_url = models.URLField(blank=True)
    sent_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'invoices_receipt'
        ordering = ['-created_at']

    def __str__(self):
        return f"Receipt {self.receipt_number}"
