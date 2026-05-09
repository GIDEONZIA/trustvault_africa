from django.db import models
from django.conf import settings
from apps.properties.models import Unit

class MaintenanceRequest(models.Model):
    CATEGORY_CHOICES = [
        ('plumbing', 'Plumbing'),
        ('electrical', 'Electrical'),
        ('structural', 'Structural'),
        ('appliance', 'Appliance'),
        ('security', 'Security'),
        ('cleaning', 'Cleaning'),
        ('other', 'Other'),
    ]
    
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('emergency', 'Emergency'),
    ]
    
    STATUS_CHOICES = [
        ('submitted', 'Submitted'),
        ('under_review', 'Under Review'),
        ('approved', 'Approved'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
        ('rejected', 'Rejected'),
    ]

    unit = models.ForeignKey(Unit, on_delete=models.RESTRICT, related_name='maintenance_requests')
    tenant = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.RESTRICT, 
        related_name='my_maintenance_requests'
    )
    
    # Request Details
    request_number = models.CharField(max_length=50, unique=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='medium')
    
    # Status & Assignment
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='submitted')
    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='assigned_tasks',
        limit_choices_to={'user_type': 'vendor'}
    )
    landlord_notes = models.TextField(blank=True, null=True)
    
    # Financial
    cost_estimate = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    actual_cost = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    invoice_generated = models.BooleanField(default=False)
    
    # Feedback & Media
    tenant_rating = models.IntegerField(null=True, blank=True)
    tenant_feedback = models.TextField(blank=True, null=True)
    photos = models.JSONField(default=list, blank=True)
    completion_photos = models.JSONField(default=list, blank=True)
    
    # Workflow Dates
    submitted_at = models.DateTimeField(auto_now_add=True)
    reviewed_at = models.DateTimeField(null=True, blank=True)
    started_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-priority', '-submitted_at']
        indexes = [
            models.Index(fields=['unit']),
            models.Index(fields=['tenant']),
            models.Index(fields=['status']),
            models.Index(fields=['priority']),
        ]

    def __str__(self):
        return f"{self.request_number}: {self.title}"
