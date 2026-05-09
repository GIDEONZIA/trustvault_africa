from celery import shared_task
from django.utils import timezone
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from apps.tenants.models import Lease
from apps.invoices.models import Invoice

@shared_task(bind=True, max_retries=3)
def generate_monthly_invoices(self, month=None, year=None):
    """Generate invoices for all active leases at the start of the month"""
    now = timezone.now()
    month = month or now.month
    year = year or now.year
    
    try:
        leases = Lease.objects.filter(status='active')
        invoices_created = 0
        
        for lease in leases:
            # Check if an invoice for this month/year already exists
            if not Invoice.objects.filter(
                lease=lease, 
                issue_date__month=month, 
                issue_date__year=year,
                invoice_type='rent'
            ).exists():
                # Create the invoice
                Invoice.objects.create(
                    lease=lease,
                    amount=lease.monthly_rent,
                    invoice_type='rent',
                    due_date=lease.start_date.replace(year=year, month=month), # Simplified due date
                    description=f"Rent for {lease.unit} - {month}/{year}"
                )
                invoices_created += 1
                
        return {'status': 'success', 'invoices_created': invoices_created}
    except Exception as exc:
        self.retry(exc=exc, countdown=60)
