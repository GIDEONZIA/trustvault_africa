from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User, LandlordProfile, TenantProfile


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Auto-create profile when user is created"""
    if created:
        if instance.is_landlord:
            LandlordProfile.objects.get_or_create(
                user=instance,
                defaults={'phone_number': instance.phone_number or ''}
            )
        elif instance.is_tenant:
            TenantProfile.objects.get_or_create(
                user=instance,
                defaults={'phone_number': instance.phone_number or ''}
            )


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """Save profile when user is saved"""
    if hasattr(instance, 'landlord_profile'):
        instance.landlord_profile.save()
    elif hasattr(instance, 'tenant_profile'):
        instance.tenant_profile.save()