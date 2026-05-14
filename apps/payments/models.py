from django.db import models

from apps.accounts.models import User
from apps.invoices.models import Invoice


class Payment(models.Model):
    METHOD_CHOICES = [
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
    tenant = models.ForeignKey(User, on_delete=models.RESTRICT, related_name='payments')

    amount = models.DecimalField(max_digits=12, decimal_places=2)
    payment_method = models.CharField(max_length=50, choices=METHOD_CHOICES, default='mpesa')

    transaction_id = models.CharField(max_length=100, unique=True, blank=True, null=True)
    mpesa_receipt = models.CharField(max_length=100, blank=True, default='')
    phone_number = models.CharField(max_length=15, blank=True, default='')
    checkout_request_id = models.CharField(max_length=100, blank=True, default='')
    merchant_request_id = models.CharField(max_length=100, blank=True, default='')

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    processed_at = models.DateTimeField(blank=True, null=True)
    failure_reason = models.TextField(blank=True, default='')

    raw_response = models.JSONField(default=dict, blank=True)
    ip_address = models.GenericIPAddressField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Payment {self.transaction_id or self.pk} - {self.status}"


class Receipt(models.Model):
    payment = models.OneToOneField(Payment, on_delete=models.RESTRICT, related_name='receipt')

    receipt_number = models.CharField(max_length=50, unique=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    payment_date = models.DateTimeField()

    tenant_name = models.CharField(max_length=255)
    property_name = models.CharField(max_length=255)
    unit_number = models.CharField(max_length=50)
    invoice_number = models.CharField(max_length=50)

    pdf_url = models.URLField(blank=True, default='')

    generated_at = models.DateTimeField(auto_now_add=True)
    sent_at = models.DateTimeField(blank=True, null=True)
    email_sent = models.BooleanField(default=False)
    sms_sent = models.BooleanField(default=False)

    def __str__(self):
        return self.receipt_number

    def save(self, *args, **kwargs):
        if not self.receipt_number:
            from django.utils import timezone
            year = timezone.now().year
            last = Receipt.objects.filter(
                receipt_number__startswith=f'RCP-{year}'
            ).order_by('-receipt_number').first()
            if last:
                num = int(last.receipt_number.split('-')[-1]) + 1
            else:
                num = 1
            self.receipt_number = f'RCP-{year}-{num:04d}'
        super().save(*args, **kwargs)
