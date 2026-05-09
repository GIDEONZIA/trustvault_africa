import uuid
from django.db import models
from django.utils import timezone
from apps.tenants.models import Lease

class Invoice(models.Model):
    INVOICE_TYPES = [
        ('rent', 'Rent'),
        ('deposit', 'Deposit'),
        ('utility', 'Utility'),
        ('maintenance', 'Maintenance'),
        ('late_fee', 'Late Fee'),
        ('other', 'Other'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('partially_paid', 'Partially Paid'),
        ('paid', 'Paid'),
        ('overdue', 'Overdue'),
        ('cancelled', 'Cancelled'),
        ('waived', 'Waived'),
    ]

    lease = models.ForeignKey(Lease, on_delete=models.RESTRICT, related_name='invoices')
    
    # Invoice Details
    invoice_number = models.CharField(max_length=50, unique=True)
    invoice_type = models.CharField(max_length=50, choices=INVOICE_TYPES)
    
    # Financial
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    amount_paid = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    # We calculate balance in a property/save method instead of STORED SQL
    
    # Dates
    issue_date = models.DateField(default=timezone.now)
    due_date = models.DateField()
    paid_date = models.DateField(null=True, blank=True)
    
    # Status
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    # Description
    description = models.TextField()
    line_items = models.JSONField(default=list, blank=True)
    
    # Late fee
    late_fee_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    late_fee_applied = models.BooleanField(default=False)
    
    # Notifications & M-Pesa
    reminder_count = models.IntegerField(default=0)
    last_reminder_sent = models.DateTimeField(null=True, blank=True)
    mpesa_checkout_request_id = models.CharField(max_length=100, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-due_date']
        indexes = [
            models.Index(fields=['lease']),
            models.Index(fields=['status']),
            models.Index(fields=['due_date']),
        ]

    def __str__(self):
        return f"{self.invoice_number} ({self.lease.unit.unit_number})"

    @property
    def balance(self):
        return self.amount - self.amount_paid
    
    def save(self, *args, **kwargs):
        if not self.invoice_number:
            # Generates a number like INV-20260509-A1B2
            date_str = timezone.now().strftime('%Y%m%d')
            unique_id = str(uuid.uuid4())[:4].upper()
            self.invoice_number = f"INV-{date_str}-{unique_id}"
            
        # Business Rule: Ensure balance is never negative
        if self.amount_paid > self.amount:
             self.amount_paid = self.amount
             
        super().save(*args, **kwargs)


class Receipt(models.Model):
    payment = models.OneToOneField(
        'payments.Payment', # <--- Use a string here instead of the class
        on_delete=models.RESTRICT, 
        related_name='receipt'
    )
    
    # Receipt Details
    receipt_number = models.CharField(max_length=50, unique=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    payment_date = models.DateTimeField()
    
    # Snapshot Info (captured at time of payment)
    tenant_name = models.CharField(max_length=255)
    property_name = models.CharField(max_length=255)
    unit_number = models.CharField(max_length=50)
    invoice_number = models.CharField(max_length=50)
    
    # Delivery & Media
    pdf_url = models.URLField(max_length=500, blank=True, null=True)
    generated_at = models.DateTimeField(auto_now_add=True)
    sent_at = models.DateTimeField(null=True, blank=True)
    email_sent = models.BooleanField(default=False)
    sms_sent = models.BooleanField(default=False)

    class Meta:
        ordering = ['-generated_at']
        indexes = [
            models.Index(fields=['payment']),
            models.Index(fields=['receipt_number']),
        ]

    def __str__(self):
        return f"{self.receipt_number} - {self.tenant_name}"

    def mark_as_paid(self):
        self.status = 'paid'
        self.amount_paid = self.amount
        self.paid_date = timezone.now().date()
        self.save()