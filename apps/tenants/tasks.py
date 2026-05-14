import datetime

from celery import shared_task


@shared_task
def check_expiring_leases():
    from .models import Lease
    threshold = datetime.date.today() + datetime.timedelta(days=30)
    expiring = Lease.objects.filter(
        status='active',
        end_date__lte=threshold,
        end_date__gte=datetime.date.today(),
    ).select_related('tenant', 'unit', 'unit__building')

    for lease in expiring:
        pass  # TODO: send notification to landlord & tenant
    return f"Found {expiring.count()} expiring leases"
