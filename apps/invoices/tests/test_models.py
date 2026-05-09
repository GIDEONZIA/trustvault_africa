from django.test import TestCase
from apps.invoices.models import Invoice
from .factories import LeaseFactory

class InvoiceModelTests(TestCase):
    def setUp(self):
        # We need at least one unit/property in DB for the factory to work
        self.lease = LeaseFactory()

    def test_invoice_number_generation(self):
        invoice = Invoice.objects.create(
            lease=self.lease,
            amount=35000,
            invoice_type='rent',
            due_date='2026-06-01',
            description='Test Rent'
        )
        # Note: Ensure your Invoice model actually has logic to auto-generate this!
        self.assertTrue(invoice.invoice_number.startswith('INV-'))
