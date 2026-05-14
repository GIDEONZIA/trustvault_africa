import datetime

from celery import shared_task
from django.utils import timezone


@shared_task
def generate_monthly_invoices():
    from apps.tenants.models import Lease
    from .models import Invoice

    today = timezone.now().date()
    active_leases = Lease.objects.filter(status='active').select_related('unit', 'unit__building', 'tenant')
    created_count = 0

    for lease in active_leases:
        due_date = today.replace(day=min(lease.payment_day, 28))
        month_desc = today.strftime('%B %Y')

        existing = Invoice.objects.filter(
            lease=lease,
            invoice_type='rent',
            due_date__month=today.month,
            due_date__year=today.year,
        ).exists()

        if not existing:
            Invoice.objects.create(
                lease=lease,
                invoice_type='rent',
                amount=lease.monthly_rent,
                due_date=due_date,
                description=f'{month_desc} Rent - {lease.unit}',
            )
            created_count += 1

    return f"Generated {created_count} invoices"


@shared_task
def send_rent_reminders():
    from .models import Invoice

    today = datetime.date.today()
    upcoming = Invoice.objects.filter(
        status='pending',
        due_date__lte=today + datetime.timedelta(days=3),
        due_date__gte=today,
    ).select_related('lease', 'lease__tenant')

    overdue = Invoice.objects.filter(
        status__in=['pending', 'partially_paid'],
        due_date__lt=today,
    ).select_related('lease', 'lease__tenant')

    count = 0
    for invoice in list(upcoming) + list(overdue):
        invoice.reminder_count += 1
        invoice.last_reminder_sent = timezone.now()
        invoice.save()
        count += 1

    return f"Sent {count} reminders"


@shared_task
def mark_overdue_invoices():
    import datetime as dt
    from .models import Invoice

    today = dt.date.today()
    updated = Invoice.objects.filter(
        status__in=['pending', 'partially_paid'],
        due_date__lt=today,
    ).update(status='overdue')

    return f"Marked {updated} invoices as overdue"
