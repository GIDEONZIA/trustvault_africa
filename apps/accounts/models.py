from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    # Remove username as we use email for login
    username = None
    email = models.EmailField(unique=True)
    
    # Custom KYC and Identity
    phone_number = models.CharField(max_length=15, unique=True)
    id_number = models.CharField(max_length=20, unique=True, null=True, blank=True)
    
    USER_TYPE_CHOICES = [
        ('landlord', 'Landlord'),
        ('tenant', 'Tenant'),
        ('vendor', 'Vendor'),
        ('admin', 'Admin'),
    ]
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES)
    
    # Profile & Verification
    is_verified = models.BooleanField(default=False)
    profile_photo = models.URLField(max_length=500, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    emergency_contact = models.CharField(max_length=15, null=True, blank=True)
    
    # Subscription logic for SaaS
    PLAN_CHOICES = [
        ('free', 'Free'),
        ('pro', 'Pro'),
        ('enterprise', 'Enterprise'),
    ]
    subscription_plan = models.CharField(max_length=20, choices=PLAN_CHOICES, default='free')
    subscription_expires = models.DateTimeField(null=True, blank=True)
    max_properties = models.IntegerField(default=1)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'phone_number']

    def __str__(self):
        return f"{self.email} ({self.user_type})"
