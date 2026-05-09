from django.db import models
from django.conf import settings
from django.urls import reverse

class Property(models.Model):
    PROPERTY_TYPES = [
        ('apartment', 'Apartment'),
        ('house', 'House'),
        ('commercial', 'Commercial'),
        ('mixed', 'Mixed Use'),
    ]

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='properties'
    )
    
    # Basic Info
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, max_length=255)
    description = models.TextField(blank=True, null=True)
    property_type = models.CharField(max_length=50, choices=PROPERTY_TYPES)

    # Location
    address = models.TextField()
    city = models.CharField(max_length=100)
    county = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20, blank=True, null=True)
    latitude = models.DecimalField(max_digits=10, decimal_places=8, null=True, blank=True)
    longitude = models.DecimalField(max_digits=11, decimal_places=8, null=True, blank=True)

    # Details
    year_built = models.IntegerField(null=True, blank=True)
    amenities = models.JSONField(default=dict, blank=True)
    rules = models.TextField(blank=True, null=True)

    # Media
    cover_photo = models.URLField(max_length=500, blank=True, null=True)
    photo_gallery = models.JSONField(default=list, blank=True)

    # Status
    is_active = models.BooleanField(default=True)
    is_listed = models.BooleanField(default=False)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = 'properties'
        verbose_name_plural = 'properties'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['owner']),
            models.Index(fields=['city']),
            models.Index(fields=['property_type']),
        ]

    def __str__(self) -> str:
        return f"{self.name} ({self.city})"

    @property
    def total_units_count(self) -> int:
        return self.units.count()  # type: ignore[attr-defined]


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

    property = models.ForeignKey(
        'Property', 
        on_delete=models.CASCADE, 
        related_name='units'
    )
    
    # Identification
    unit_number = models.CharField(max_length=50)
    unit_type = models.CharField(max_length=50, choices=UNIT_TYPES)
    
    # Specifications
    bedrooms = models.IntegerField(default=0)
    bathrooms = models.IntegerField(default=0)
    square_footage = models.IntegerField(null=True, blank=True)
    floor_number = models.IntegerField(null=True, blank=True)
    is_furnished = models.BooleanField(default=False)

    # Financial
    monthly_rent = models.DecimalField(max_digits=12, decimal_places=2)
    deposit_amount = models.DecimalField(max_digits=12, decimal_places=2)
    deposit_terms = models.TextField(blank=True, null=True)

    # Amenities & Media
    unit_amenities = models.JSONField(default=list, blank=True)
    photos = models.JSONField(default=list, blank=True)
    video_tour = models.URLField(max_length=500, blank=True, null=True)

    # Status
    is_available = models.BooleanField(default=True)
    available_from = models.DateField(null=True, blank=True)

    # Public Listing
    listing_title = models.CharField(max_length=255, blank=True, null=True)
    listing_description = models.TextField(blank=True, null=True)
    is_published = models.BooleanField(default=False)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = 'properties'
        ordering = ['floor_number', 'unit_number']
        unique_together = ('property', 'unit_number')
        indexes = [
            models.Index(fields=['property']),
            models.Index(fields=['is_available']),
            models.Index(fields=['is_published']),
            models.Index(fields=['monthly_rent']),
        ]

    def __str__(self):
        return f"{self.property.name} - {self.unit_number}"
