from django.db import models
from django.urls import reverse
from django.utils.text import slugify

from apps.accounts.models import User


class Property(models.Model):
    PROPERTY_TYPES = [
        ('apartment', 'Apartment'),
        ('house', 'House'),
        ('commercial', 'Commercial'),
        ('mixed', 'Mixed Use'),
    ]

    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='properties',
        limit_choices_to={'user_type': 'landlord'},
    )
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField(blank=True, default='')
    property_type = models.CharField(max_length=50, choices=PROPERTY_TYPES)

    address = models.TextField()
    city = models.CharField(max_length=100)
    county = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20, blank=True, default='')
    latitude = models.DecimalField(max_digits=10, decimal_places=8, blank=True, null=True)
    longitude = models.DecimalField(max_digits=11, decimal_places=8, blank=True, null=True)

    year_built = models.IntegerField(blank=True, null=True)
    amenities = models.JSONField(default=list, blank=True)
    rules = models.TextField(blank=True, default='')

    cover_photo = models.ImageField(upload_to='properties/', blank=True, null=True)
    photo_gallery = models.JSONField(default=list, blank=True)

    is_active = models.BooleanField(default=True)
    is_listed = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'properties'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} ({self.city})"

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 1
            while Property.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('properties:detail', kwargs={'slug': self.slug})

    @property
    def total_units(self):
        return self.units.count()

    @property
    def available_units(self):
        return self.units.filter(is_available=True).count()

    @property
    def occupied_units(self):
        return self.total_units - self.available_units

    @property
    def occupancy_rate(self):
        total = self.total_units
        if total == 0:
            return 0.0
        return round((self.occupied_units / total) * 100, 1)

    @property
    def monthly_revenue(self):
        from apps.tenants.models import Lease
        active_leases = Lease.objects.filter(
            unit__building=self, status='active'
        )
        return sum(lease.monthly_rent for lease in active_leases)


class Unit(models.Model):
    UNIT_TYPES = [
        ('studio', 'Studio'),
        ('1_bedroom', '1 Bedroom'),
        ('2_bedroom', '2 Bedroom'),
        ('3_bedroom', '3 Bedroom'),
        ('4_bedroom', '4 Bedroom'),
        ('shop', 'Shop'),
        ('office', 'Office'),
        ('warehouse', 'Warehouse'),
    ]

    building = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='units', db_column='property_id')
    unit_number = models.CharField(max_length=50)
    unit_type = models.CharField(max_length=50, choices=UNIT_TYPES)

    bedrooms = models.IntegerField(default=0)
    bathrooms = models.IntegerField(default=0)
    square_footage = models.IntegerField(blank=True, null=True)
    floor_number = models.IntegerField(blank=True, null=True)
    is_furnished = models.BooleanField(default=False)

    monthly_rent = models.DecimalField(max_digits=12, decimal_places=2)
    deposit_amount = models.DecimalField(max_digits=12, decimal_places=2)
    deposit_terms = models.TextField(blank=True, default='')

    unit_amenities = models.JSONField(default=list, blank=True)
    photos = models.JSONField(default=list, blank=True)
    video_tour = models.URLField(blank=True, default='')

    is_available = models.BooleanField(default=True)
    available_from = models.DateField(blank=True, null=True)

    listing_title = models.CharField(max_length=255, blank=True, default='')
    listing_description = models.TextField(blank=True, default='')
    is_published = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['building', 'unit_number']
        ordering = ['unit_number']

    def __str__(self):
        return f"{self.building.name} - {self.unit_number}"

    @property
    def current_tenant(self):
        from apps.tenants.models import Lease
        active_lease = Lease.objects.filter(
            unit=self, status='active'
        ).select_related('tenant').first()
        return active_lease.tenant if active_lease else None

    @property
    def current_lease(self):
        from apps.tenants.models import Lease
        return Lease.objects.filter(unit=self, status='active').first()
