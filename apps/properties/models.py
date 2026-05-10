from django.db import models
from django.core.validators import MinValueValidator
from apps.core.models import TimestampedModel


class Property(TimestampedModel):
    PROPERTY_TYPES = [
        ('apartment', 'Apartment Building'),
        ('bungalow', 'Bungalow'),
        ('maisonette', 'Maisonette'),
        ('commercial', 'Commercial Space'),
        ('hostel', 'Hostel/Bedsitter'),
    ]

    landlord = models.ForeignKey(
        'accounts.User',
        on_delete=models.CASCADE,
        related_name='properties'
    )
    name = models.CharField(max_length=255)
    address = models.TextField()
    city = models.CharField(max_length=100)
    county = models.CharField(max_length=100)
    property_type = models.CharField(max_length=20, choices=PROPERTY_TYPES)
    description = models.TextField(blank=True)
    
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    
    management_fee_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    is_active = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'properties_property'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} - {self.city}"


class Unit(TimestampedModel):
    UNIT_TYPES = [
        ('bedsitter', 'Bedsitter'),
        ('1_bedroom', '1 Bedroom'),
        ('2_bedroom', '2 Bedroom'),
        ('3_bedroom', '3 Bedroom'),
        ('4_bedroom', '4 Bedroom+'),
        ('shop', 'Shop/Retail'),
        ('office', 'Office Space'),
    ]

    property = models.ForeignKey(
        Property,
        on_delete=models.CASCADE,
        related_name='units'
    )
    unit_number = models.CharField(max_length=50)
    unit_type = models.CharField(max_length=20, choices=UNIT_TYPES)
    
    bedrooms = models.PositiveIntegerField(default=0)
    bathrooms = models.PositiveIntegerField(default=1)
    square_footage = models.PositiveIntegerField(null=True, blank=True)
    
    monthly_rent = models.DecimalField(max_digits=12, decimal_places=2)
    deposit_amount = models.DecimalField(max_digits=12, decimal_places=2)
    
    is_available = models.BooleanField(default=True)
    available_from = models.DateField(null=True, blank=True)
    
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'properties_unit'
        ordering = ['unit_number']

    def __str__(self):
        return f"{self.property.name} - Unit {self.unit_number}"


class Amenity(TimestampedModel):
    unit = models.ForeignKey(
        Unit,
        on_delete=models.CASCADE,
        related_name='amenities'
    )
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    class Meta:
        db_table = 'properties_amenity'

    def __str__(self):
        return self.name


class PropertyImage(TimestampedModel):
    unit = models.ForeignKey(
        Unit,
        on_delete=models.CASCADE,
        related_name='images'
    )
    image_url = models.URLField()
    is_primary = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'properties_property_image'

    def __str__(self):
        return f"Image for {self.unit}"
