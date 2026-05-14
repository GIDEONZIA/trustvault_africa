from django.db import models
from django.utils import timezone

from apps.tenants.models import Lease


class Invoice(models.Model):
    TYPE_CHOICES = [
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

    invoice_number = models.CharField(max_length=50, unique=True)
    invoice_type = models.CharField(max_length=50, choices=TYPE_CHOICES, default='rent')

    amount = models.DecimalField(max_digits=12, decimal_places=2)
    amount_paid = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    issue_date = models.DateField(default=timezone.now)
    due_date = models.DateField()
    paid_date = models.DateField(blank=True, null=True)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    description = models.TextField()
    line_items = models.JSONField(default=list, blank=True)

    late_fee_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    late_fee_applied = models.BooleanField(default=False)

    reminder_count = models.IntegerField(default=0)
    last_reminder_sent = models.DateTimeField(blank=True, null=True)

    mpesa_checkout_request_id = models.CharField(max_length=100, blank=True, default='')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-due_date']

    def __str__(self):
        return f"{self.invoice_number} - {self.status}"

    def save(self, *args, **kwargs):
        if not self.invoice_number:
            year = timezone.now().year
            last = Invoice.objects.filter(
                invoice_number__startswith=f'INV-{year}'
            ).order_by('-invoice_number').first()
            if last:
                num = int(last.invoice_number.split('-')[-1]) + 1
            else:
                num = 1
            self.invoice_number = f'INV-{year}-{num:04d}'
        super().save(*args, **kwargs)

    @property
    def balance(self):
        return self.amount - self.amount_paid

    @property
    def is_overdue(self):
        import datetime
        return self.due_date < datetime.date.today() and self.status in ['pending', 'partially_paid']

    @property
    def days_overdue(self):
        import datetime
        if self.is_overdue:
            return (datetime.date.today() - self.due_date).days
        return 0

    def record_payment(self, amount):
        self.amount_paid += amount
        if self.amount_paid >= self.amount:
            self.status = 'paid'
            self.paid_date = timezone.now().date()
        elif self.amount_paid > 0:
            self.status = 'partially_paid'
        self.save()


class InvoiceReminder(models.Model):
    CHANNEL_CHOICES = [
        ('sms', 'SMS'),
        ('email', 'Email'),
        ('both', 'Both'),
    ]

    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name='reminders')
    reminder_type = models.CharField(max_length=50, default='payment_due')
    sent_at = models.DateTimeField(auto_now_add=True)
    channel = models.CharField(max_length=10, choices=CHANNEL_CHOICES, default='sms')
    status = models.CharField(max_length=20, default='sent')
    failure_reason = models.TextField(blank=True, default='')

    def __str__(self):
        return f"Reminder for {self.invoice.invoice_number}"
