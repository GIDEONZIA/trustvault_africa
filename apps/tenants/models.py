from django.db import models
from django.conf import settings
from apps.properties.models import Unit
from django.core.exceptions import ValidationError
from django.db.models import Q

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
    tenant = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.RESTRICT, 
        related_name='tenant_leases',
        limit_choices_to={'user_type': 'tenant'}
    )
    
    # Lease Terms
    lease_number = models.CharField(max_length=50, unique=True)
    start_date = models.DateField()
    end_date = models.DateField()
    monthly_rent = models.DecimalField(max_digits=12, decimal_places=2)
    payment_day = models.IntegerField(default=5) # 1-28 check handled in clean() or validators

    # Financial
    deposit_paid = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    deposit_status = models.CharField(
        max_length=20, 
        choices=DEPOSIT_STATUS_CHOICES, 
        default='pending'
    )

    # Status & Renewals
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    is_renewable = models.BooleanField(default=True)
    auto_renew = models.BooleanField(default=False)

    # Documents
    lease_document = models.URLField(max_length=500, blank=True, null=True)
    terms_accepted = models.BooleanField(default=False)

    # Termination
    termination_date = models.DateField(null=True, blank=True)
    termination_reason = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-start_date']
        indexes = [
            models.Index(fields=['tenant']),
            models.Index(fields=['unit']),
            models.Index(fields=['status']),
            models.Index(fields=['start_date', 'end_date']),
        ]
        constraints = [
            # Ensures only one 'active' lease exists per unit at a time
            models.UniqueConstraint(
                fields=['unit'], 
                condition=models.Q(status='active'), 
                name='unique_active_lease_per_unit'
            )
        ]

    def __str__(self):
        return f"{self.lease_number} - {self.unit.unit_number}"

class TenantProfile(models.Model):
    EMPLOYMENT_TYPES = [
        ('full_time', 'Full Time'),
        ('part_time', 'Part Time'),
        ('self_employed', 'Self Employed'),
        ('student', 'Student'),
    ]

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='tenant_profile',
        limit_choices_to={'user_type': 'tenant'}
    )
    
    # Employment
    employer_name = models.CharField(max_length=255, blank=True, null=True)
    employer_address = models.TextField(blank=True, null=True)
    job_title = models.CharField(max_length=100, blank=True, null=True)
    monthly_income = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    employment_type = models.CharField(max_length=50, choices=EMPLOYMENT_TYPES, blank=True, null=True)

    # References
    emergency_contact_name = models.CharField(max_length=255, blank=True, null=True)
    emergency_contact_phone = models.CharField(max_length=15, blank=True, null=True)
    referee_name = models.CharField(max_length=255, blank=True, null=True)
    referee_phone = models.CharField(max_length=15, blank=True, null=True)

    # Documents
    id_document = models.URLField(max_length=500, blank=True, null=True)
    employment_letter = models.URLField(max_length=500, blank=True, null=True)

    # Rating
    tenant_score = models.DecimalField(max_digits=3, decimal_places=2, default=5.00)
    payment_history_score = models.IntegerField(default=100)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Profile: {self.user.email}"

    