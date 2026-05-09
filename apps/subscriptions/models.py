from django.db import models
from django.conf import settings

class Subscription(models.Model):
    PLAN_TYPES = [
        ('free', 'Free'),
        ('pro', 'Pro'),
        ('enterprise', 'Enterprise'),
    ]
    
    BILLING_CYCLES = [
        ('monthly', 'Monthly'),
        ('annual', 'Annual'),
    ]
    
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('cancelled', 'Cancelled'),
        ('past_due', 'Past Due'),
        ('trialing', 'Trialing'),
    ]

    landlord = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='subscription_record',
        limit_choices_to={'user_type': 'landlord'}
    )
    
    # Plan & Cycle
    plan_type = models.CharField(max_length=20, choices=PLAN_TYPES)
    billing_cycle = models.CharField(max_length=20, choices=BILLING_CYCLES, default='monthly')
    
    # Pricing
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    currency = models.CharField(max_length=3, default='KES')
    
    # Status
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    
    # Dates
    current_period_start = models.DateField()
    current_period_end = models.DateField()
    trial_ends_at = models.DateTimeField(null=True, blank=True)
    cancelled_at = models.DateTimeField(null=True, blank=True)
    
    # M-Pesa & Renewals
    mpesa_phone = models.CharField(max_length=15, blank=True, null=True)
    auto_renew = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.landlord.email} - {self.plan_type} ({self.status})"
