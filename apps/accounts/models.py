from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email is required')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('user_type', 'admin')
        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    USER_TYPE_CHOICES = [
        ('landlord', 'Landlord'),
        ('tenant', 'Tenant'),
        ('vendor', 'Vendor'),
        ('admin', 'Admin'),
    ]
    SUBSCRIPTION_CHOICES = [
        ('free', 'Free'),
        ('pro', 'Pro'),
        ('enterprise', 'Enterprise'),
    ]

    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    phone_number = models.CharField(max_length=15, unique=True, blank=True, null=True)
    id_number = models.CharField(max_length=20, unique=True, blank=True, null=True)
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES, default='landlord')

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)

    profile_photo = models.ImageField(upload_to='profiles/', blank=True, null=True)
    address = models.TextField(blank=True, default='')
    emergency_contact = models.CharField(max_length=15, blank=True, default='')

    subscription_plan = models.CharField(max_length=20, choices=SUBSCRIPTION_CHOICES, default='free')
    subscription_expires = models.DateTimeField(blank=True, null=True)
    max_properties = models.IntegerField(default=1)

    date_joined = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    class Meta:
        ordering = ['-date_joined']

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def is_landlord(self):
        return self.user_type == 'landlord'

    @property
    def is_tenant(self):
        return self.user_type == 'tenant'

    @property
    def is_vendor(self):
        return self.user_type == 'vendor'
