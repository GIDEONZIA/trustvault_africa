"""Celery configuration for RentFlow."""

import os

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.development')

app = Celery('rentflow')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'generate-monthly-invoices': {
        'task': 'apps.invoices.tasks.generate_monthly_invoices',
        'schedule': crontab(day_of_month='1', hour='0', minute='0'),
    },
    'send-rent-reminders': {
        'task': 'apps.invoices.tasks.send_rent_reminders',
        'schedule': crontab(hour='8', minute='0'),
    },
    'mark-overdue-invoices': {
        'task': 'apps.invoices.tasks.mark_overdue_invoices',
        'schedule': crontab(hour='0', minute='30'),
    },
    'check-expiring-leases': {
        'task': 'apps.tenants.tasks.check_expiring_leases',
        'schedule': crontab(hour='9', minute='0'),
    },
}
