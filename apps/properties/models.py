from django.db import models
from django.core.validators import MinValueValidator
from apps.core.models import TimestampedModel


class Property(TimestampedModel):
    """
    A rental property or building owned by a landlord.
    """
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
        related_name='properties',
        limit_choices_to={'is_landlord': True}
    )
    name = models.CharField(max_length=255)
    address = models.TextField()
    city = models.CharField(max_length=100)
    county = models.CharField(max_length=100)
    property_type = models.CharField(max_length=20, choices=PROPERTY_TYPES)
    description = models.TextField(blank=True)
    
    # Location
    latitude = models.DecimalField(
        max_digits=9, 
        decimal_places=6, 
        null=True, 
        blank=True
    )
    longitude = models.DecimalField(
        max_digits=9, 
        decimal_places=6, 
        null=True, 
        blank=True
    )
    
    # Management
    management_fee_percentage = models.DecimalField(
        max_digits=5, 
        decimal_places=2, 
        default=0
    )
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'properties_property'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} - {self.city}"

    @property
    def unit_count(self):
        return self.units.count()

    @property
    def occupied_units(self):
        return self.units.filter(is_available=False).count()


class Unit(TimestampedModel):
    """
    Individual rental unit within a property.
    """
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
    
    # Specifications
    bedrooms = models.PositiveIntegerField(default=0)
    bathrooms = models.PositiveIntegerField(default=1)
    square_footage = models.PositiveIntegerField(null=True, blank=True)
    
    # Financial
    monthly_rent = models.DecimalField(
        max_digits=12, 
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    deposit_amount = models.DecimalField(
        max_digits=12, 
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    
    # Status
    is_available = models.BooleanField(default=True)
    available_from = models.DateField(null=True, blank=True)
    description = models.TextField(blank=True)

    class Meta:
        db_table = 'properties_unit'
        ordering = ['unit_number']

    def __str__(self):
        return f"{self.property.name} - Unit {self.unit_number}"


class Amenity(TimestampedModel):
    """
    Amenities available in a unit.
    """
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
    """
    Photos of properties and units.
    """
    property = models.ForeignKey(
        Property,
        on_delete=models.CASCADE,
        related_name='images',
        null=True,
        blank=True
    )
    unit = models.ForeignKey(
        Unit,
        on_delete=models.CASCADE,
        related_name='images',
        null=True,
        blank=True
    )
    image = models.ImageField(upload_to='properties/%Y/%m/')
    caption = models.CharField(max_length=255, blank=True)
    is_primary = models.BooleanField(default=False)

    class Meta:
        db_table = 'properties_image'

    def __str__(self):
        return f"Image for {self.property or self.unit}"
