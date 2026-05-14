from django.db import models

from apps.accounts.models import User
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
    tenant = models.ForeignKey(User, on_delete=models.RESTRICT, related_name='maintenance_requests')

    request_number = models.CharField(max_length=50, unique=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='medium')

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='submitted')

    assigned_to = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='assigned_maintenance',
    )
    landlord_notes = models.TextField(blank=True, default='')

    cost_estimate = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    actual_cost = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    invoice_generated = models.BooleanField(default=False)

    tenant_rating = models.IntegerField(blank=True, null=True)
    tenant_feedback = models.TextField(blank=True, default='')

    photos = models.JSONField(default=list, blank=True)
    completion_photos = models.JSONField(default=list, blank=True)

    submitted_at = models.DateTimeField(auto_now_add=True)
    reviewed_at = models.DateTimeField(blank=True, null=True)
    started_at = models.DateTimeField(blank=True, null=True)
    completed_at = models.DateTimeField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.request_number} - {self.title}"

    def save(self, *args, **kwargs):
        if not self.request_number:
            from django.utils import timezone
            year = timezone.now().year
            last = MaintenanceRequest.objects.filter(
                request_number__startswith=f'MR-{year}'
            ).order_by('-request_number').first()
            if last:
                num = int(last.request_number.split('-')[-1]) + 1
            else:
                num = 1
            self.request_number = f'MR-{year}-{num:04d}'
        super().save(*args, **kwargs)

    @property
    def days_open(self):
        import datetime
        if self.completed_at:
            return (self.completed_at.date() - self.submitted_at.date()).days
        return (datetime.date.today() - self.submitted_at.date()).days
