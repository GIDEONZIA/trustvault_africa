from django.db import models
from django.core.validators import MinValueValidator
from apps.core.models import TimestampedModel


class MaintenanceRequest(TimestampedModel):
    """
    Tenant maintenance/repair request.
    """
    CATEGORY_CHOICES = [
        ('plumbing', 'Plumbing'),
        ('electrical', 'Electrical'),
        ('carpentry', 'Carpentry'),
        ('painting', 'Painting'),
        ('appliance', 'Appliance Repair'),
        ('structural', 'Structural'),
        ('cleaning', 'Cleaning'),
        ('other', 'Other'),
    ]

    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('urgent', 'Urgent'),
    ]

    STATUS_CHOICES = [
        ('submitted', 'Submitted'),
        ('under_review', 'Under Review'),
        ('approved', 'Approved'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('declined', 'Declined'),
    ]

    tenant = models.ForeignKey(
        'accounts.User',
        on_delete=models.CASCADE,
        related_name='maintenance_requests'
    )
    unit = models.ForeignKey(
        'properties.Unit',
        on_delete=models.CASCADE,
        related_name='maintenance_requests'
    )
    
    # Request details
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    description = models.TextField()
    priority = models.CharField(
        max_length=10, 
        choices=PRIORITY_CHOICES, 
        default='medium'
    )
    
    # Photos
    photo_1 = models.ImageField(upload_to='maintenance/%Y/%m/', blank=True)
    photo_2 = models.ImageField(upload_to='maintenance/%Y/%m/', blank=True)
    photo_3 = models.ImageField(upload_to='maintenance/%Y/%m/', blank=True)
    
    # Status workflow
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='submitted'
    )
    
    # Scheduling
    preferred_date = models.DateField(null=True, blank=True)
    preferred_time = models.TimeField(null=True, blank=True)
    
    # Resolution
    resolution_notes = models.TextField(blank=True)
    tenant_satisfaction = models.PositiveIntegerField(null=True, blank=True)

    class Meta:
        db_table = 'maintenance_request'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.category} - {self.unit}"


class Vendor(TimestampedModel):
    """
    Service provider directory for maintenance work.
    """
    SPECIALTY_CHOICES = [
        ('plumbing', 'Plumbing'),
        ('electrical', 'Electrical'),
        ('carpentry', 'Carpentry'),
        ('painting', 'Painting'),
        ('appliance', 'Appliance'),
        ('general', 'General'),
    ]

    landlord = models.ForeignKey(
        'accounts.User',
        on_delete=models.CASCADE,
        related_name='vendors',
        limit_choices_to={'is_landlord': True}
    )
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=15)
    email = models.EmailField(blank=True)
    specialty = models.CharField(
        max_length=20, 
        choices=SPECIALTY_CHOICES
    )
    rating = models.DecimalField(
        max_digits=3, 
        decimal_places=2, 
        null=True, 
        blank=True
    )
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'maintenance_vendor'

    def __str__(self):
        return f"{self.name} ({self.specialty})"


class MaintenanceTask(TimestampedModel):
    """
    Assigned maintenance work.
    """
    STATUS_CHOICES = [
        ('assigned', 'Assigned'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    request = models.ForeignKey(
        MaintenanceRequest,
        on_delete=models.CASCADE,
        related_name='tasks'
    )
    vendor = models.ForeignKey(
        Vendor,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='tasks'
    )
    assigned_by = models.ForeignKey(
        'accounts.User',
        on_delete=models.CASCADE,
        related_name='assigned_tasks'
    )
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES,
        default='assigned'
    )
    estimated_cost = models.DecimalField(
        max_digits=12, 
        decimal_places=2, 
        null=True, 
        blank=True
    )
    actual_cost = models.DecimalField(
        max_digits=12, 
        decimal_places=2, 
        null=True, 
        blank=True
    )
    scheduled_date = models.DateField(null=True, blank=True)
    completed_date = models.DateField(null=True, blank=True)
    notes = models.TextField(blank=True)

    class Meta:
        db_table = 'maintenance_task'

    def __str__(self):
        return f"Task for {self.request}"


class MaintenanceExpense(TimestampedModel):
    """
    Cost tracking for maintenance repairs.
    """
    task = models.ForeignKey(
        MaintenanceTask,
        on_delete=models.CASCADE,
        related_name='expenses'
    )
    amount = models.DecimalField(
        max_digits=12, 
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    description = models.CharField(max_length=255)
    receipt = models.FileField(
        upload_to='maintenance/receipts/%Y/%m/', 
        blank=True
    )

    class Meta:
        db_table = 'maintenance_expense'

    def __str__(self):
        return f"KES {self.amount} - {self.description}"
