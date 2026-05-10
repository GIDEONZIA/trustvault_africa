from django.contrib.auth.models import AbstractUser
from django.db import models
from apps.core.models import TimestampedModel


class User(AbstractUser):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    phone_number = models.CharField(max_length=15, blank=True)
    
    is_landlord = models.BooleanField(default=False)
    is_tenant = models.BooleanField(default=False)
    is_vendor = models.BooleanField(default=False)
    
    email_verified = models.BooleanField(default=False)
    phone_verified = models.BooleanField(default=False)
    
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(null=True, blank=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    class Meta:
        db_table = 'accounts_user'
        ordering = ['-date_joined']

    def __str__(self):
        return f"{self.email} - {self.first_name} {self.last_name}"


class LandlordProfile(TimestampedModel):
    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE,
        related_name='landlord_profile'
    )
    phone_number = models.CharField(max_length=15)
    id_number = models.CharField(max_length=20, blank=True)
    kra_pin = models.CharField(max_length=15, blank=True)
    bank_name = models.CharField(max_length=100, blank=True)
    bank_account = models.CharField(max_length=50, blank=True)
    subscription_tier = models.CharField(
        max_length=20,
        choices=[
            ('free', 'Free'),
            ('pro', 'Pro'),
            ('enterprise', 'Enterprise'),
        ],
        default='free'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'accounts_landlord_profile'

    def __str__(self):
        return f"Landlord: {self.user.get_full_name()}"


class TenantProfile(TimestampedModel):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='tenant_profile'
    )
    phone_number = models.CharField(max_length=15)
    emergency_name = models.CharField(max_length=150, blank=True)
    emergency_phone = models.CharField(max_length=15, blank=True)
    employer_name = models.CharField(max_length=150, blank=True)
    employer_phone = models.CharField(max_length=15, blank=True)
    monthly_income = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'accounts_tenant_profile'

    def __str__(self):
        return f"Tenant: {self.user.get_full_name()}"
