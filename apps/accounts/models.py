from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models
from apps.core.models import TimestampedModel


class CustomUserManager(UserManager):
    def create_user(self, username=None, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        
        if not email:
            raise ValueError('Email is required')
        
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, username=None, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        
        if not email:
            raise ValueError('Email is required')
        
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def landlords(self):
        """Return only landlord users"""
        return self.filter(is_landlord=True)
    
    def tenants(self):
        """Return only tenant users"""
        return self.filter(is_tenant=True)


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name="email address")
    first_name = models.CharField(max_length=150, verbose_name="first name")
    last_name = models.CharField(max_length=150, verbose_name="last name")
    phone_number = models.CharField(max_length=15, blank=True, verbose_name="phone number")
    
    # Role flags
    is_landlord = models.BooleanField(default=False, verbose_name="landlord status")
    is_tenant = models.BooleanField(default=False, verbose_name="tenant status")
    is_vendor = models.BooleanField(default=False, verbose_name="vendor status")
    
    # Verification flags
    email_verified = models.BooleanField(default=False, verbose_name="email verified")
    phone_verified = models.BooleanField(default=False, verbose_name="phone verified")
    
    # Timestamps
    date_joined = models.DateTimeField(auto_now_add=True, verbose_name="date joined")
    last_login = models.DateTimeField(null=True, blank=True, verbose_name="last login")
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']
    
    objects = CustomUserManager()
    
    class Meta:
        db_table = 'accounts_user'
        ordering = ['-date_joined']
        verbose_name = 'user'
        verbose_name_plural = 'users'
    
    def __str__(self):
        return f"{self.email} - {self.get_full_name()}"
    
    def get_full_name(self):
        """Return full name"""
        return f"{self.first_name} {self.last_name}".strip() or self.email
    
    def get_short_name(self):
        """Return short name"""
        return self.first_name or self.email
    
    @property
    def role(self):
        """Return user role as string"""
        if self.is_landlord:
            return 'landlord'
        elif self.is_tenant:
            return 'tenant'
        elif self.is_vendor:
            return 'vendor'
        return 'user'
    
    @property
    def is_profile_complete(self):
        """Check if basic profile is filled"""
        return bool(self.first_name and self.last_name and self.email)


class LandlordProfile(TimestampedModel):
    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE,
        related_name='landlord_profile',
        verbose_name="user"
    )
    phone_number = models.CharField(max_length=15, verbose_name="phone number")
    id_number = models.CharField(max_length=20, blank=True, verbose_name="ID number")
    kra_pin = models.CharField(max_length=15, blank=True, verbose_name="KRA PIN")
    bank_name = models.CharField(max_length=100, blank=True, verbose_name="bank name")
    bank_account = models.CharField(max_length=50, blank=True, verbose_name="bank account")
    subscription_tier = models.CharField(
        max_length=20,
        choices=[
            ('free', 'Free'),
            ('pro', 'Pro'),
            ('enterprise', 'Enterprise'),
        ],
        default='free',
        verbose_name="subscription tier"
    )
    
    class Meta(TimestampedModel.Meta):
        db_table = 'accounts_landlord_profile'
        verbose_name = 'landlord profile'
        verbose_name_plural = 'landlord profiles'
    
    def __str__(self):
        return f"Landlord: {self.user.get_full_name()}"
    
    @property
    def display_name(self):
        return self.user.get_full_name()


class TenantProfile(TimestampedModel):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='tenant_profile',
        verbose_name="user"
    )
    phone_number = models.CharField(max_length=15, verbose_name="phone number")
    emergency_name = models.CharField(max_length=150, blank=True, verbose_name="emergency contact name")
    emergency_phone = models.CharField(max_length=15, blank=True, verbose_name="emergency contact phone")
    employer_name = models.CharField(max_length=150, blank=True, verbose_name="employer name")
    employer_phone = models.CharField(max_length=15, blank=True, verbose_name="employer phone")
    monthly_income = models.DecimalField(
        max_digits=12, 
        decimal_places=2, 
        null=True, 
        blank=True,
        verbose_name="monthly income"
    )
    
    class Meta(TimestampedModel.Meta):
        db_table = 'accounts_tenant_profile'
        verbose_name = 'tenant profile'
        verbose_name_plural = 'tenant profiles'
    
    def __str__(self):
        return f"Tenant: {self.user.get_full_name()}"
    
    @property
    def display_name(self):
        return self.user.get_full_name()