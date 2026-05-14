import datetime

from django.db import models
from django.utils import timezone

from apps.accounts.models import User
from apps.properties.models import Unit


class Lease(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('active', 'Active'),
        ('expired', 'Expired'),
        ('terminated', 'Terminated'),
        ('renewed', 'Renewed'),
    ]
    DEPOSIT_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('partially_refunded', 'Partially Refunded'),
        ('fully_refunded', 'Fully Refunded'),
    ]

    unit = models.ForeignKey(Unit, on_delete=models.RESTRICT, related_name='leases')
    tenant = models.ForeignKey(User, on_delete=models.RESTRICT, related_name='leases', limit_choices_to={'user_type': 'tenant'})

    lease_number = models.CharField(max_length=50, unique=True)
    start_date = models.DateField()
    end_date = models.DateField()
    monthly_rent = models.DecimalField(max_digits=12, decimal_places=2)
    payment_day = models.IntegerField(default=5)

    deposit_paid = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    deposit_status = models.CharField(max_length=20, choices=DEPOSIT_STATUS_CHOICES, default='pending')

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    is_renewable = models.BooleanField(default=True)
    auto_renew = models.BooleanField(default=False)

    lease_document = models.FileField(upload_to='leases/', blank=True, null=True)
    terms_accepted = models.BooleanField(default=False)

    termination_date = models.DateField(blank=True, null=True)
    termination_reason = models.TextField(blank=True, default='')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.lease_number} - {self.tenant.full_name}"

    def save(self, *args, **kwargs):
        if not self.lease_number:
            year = timezone.now().year
            last = Lease.objects.filter(
                lease_number__startswith=f'RF-{year}'
            ).order_by('-lease_number').first()
            if last:
                num = int(last.lease_number.split('-')[-1]) + 1
            else:
                num = 1
            self.lease_number = f'RF-{year}-{num:04d}'
        super().save(*args, **kwargs)

    @property
    def days_until_expiry(self):
        if self.end_date:
            delta = self.end_date - datetime.date.today()
            return max(delta.days, 0)
        return 0

    @property
    def is_expiring_soon(self):
        return self.days_until_expiry <= 30 and self.status == 'active'

    @property
    def outstanding_balance(self):
        from apps.invoices.models import Invoice
        return Invoice.objects.filter(
            lease=self, status__in=['pending', 'partially_paid', 'overdue']
        ).aggregate(total=models.Sum('amount') - models.Sum('amount_paid'))['total'] or 0


class TenantProfile(models.Model):
    EMPLOYMENT_TYPES = [
        ('full_time', 'Full Time'),
        ('part_time', 'Part Time'),
        ('self_employed', 'Self Employed'),
        ('student', 'Student'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='tenant_profile')

    employer_name = models.CharField(max_length=255, blank=True, default='')
    employer_address = models.TextField(blank=True, default='')
    job_title = models.CharField(max_length=100, blank=True, default='')
    monthly_income = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    employment_type = models.CharField(max_length=50, choices=EMPLOYMENT_TYPES, blank=True, default='')

    emergency_contact_name = models.CharField(max_length=255, blank=True, default='')
    emergency_contact_phone = models.CharField(max_length=15, blank=True, default='')
    referee_name = models.CharField(max_length=255, blank=True, default='')
    referee_phone = models.CharField(max_length=15, blank=True, default='')

    id_document = models.FileField(upload_to='documents/', blank=True, null=True)
    employment_letter = models.FileField(upload_to='documents/', blank=True, null=True)

    tenant_score = models.DecimalField(max_digits=3, decimal_places=2, default=5.00)
    payment_history_score = models.IntegerField(default=100)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Profile: {self.user.full_name}"
