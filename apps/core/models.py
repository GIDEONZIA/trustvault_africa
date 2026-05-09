from django.db import models


class TimestampedModel(models.Model):
    """
    Abstract base model that provides created_at and updated_at timestamps.
    All models in RentFlow should inherit from this.
    """
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ['-created_at']
