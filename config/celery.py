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
        'schedule': crontab(day_of_month=1, hour=0, minute=0),
    },
    'check-overdue-invoices': {
        'task': 'apps.invoices.tasks.check_overdue_invoices', # You'll need to define this task later
        'schedule': crontab(hour=6, minute=0),
    },
}
