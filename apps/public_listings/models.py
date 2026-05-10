from django.db import models
from apps.core.models import TimestampedModel


class PublicListing(TimestampedModel):
    unit = models.OneToOneField(
        'properties.Unit',
        on_delete=models.CASCADE,
        related_name='public_listing'
    )
    title = models.CharField(max_length=255)
    description = models.TextField()
    featured_image = models.URLField()
    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    view_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'public_listing'
        ordering = ['-created_at']

    def __str__(self):
        return self.title


class Inquiry(TimestampedModel):
    STATUS_CHOICES = [
        ('new', 'New'),
        ('contacted', 'Contacted'),
        ('viewing_scheduled', 'Viewing Scheduled'),
        ('converted', 'Converted'),
        ('closed', 'Closed'),
    ]

    listing = models.ForeignKey(
        PublicListing,
        on_delete=models.CASCADE,
        related_name='inquiries'
    )
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=15)
    email = models.EmailField(blank=True)
    message = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'public_inquiry'

    def __str__(self):
        return f"Inquiry from {self.name}"


class ViewingSchedule(TimestampedModel):
    STATUS_CHOICES = [
        ('scheduled', 'Scheduled'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
        ('no_show', 'No Show'),
    ]

    inquiry = models.ForeignKey(
        Inquiry,
        on_delete=models.CASCADE,
        related_name='viewings'
    )
    scheduled_date = models.DateField()
    scheduled_time = models.TimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='scheduled')
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'public_viewing_schedule'

    def __str__(self):
        return f"Viewing on {self.scheduled_date} at {self.scheduled_time}"
