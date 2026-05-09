from django.db import models
from django.core.validators import MinValueValidator
from apps.core.models import TimestampedModel


class Lease(TimestampedModel):
    """
    Rental agreement between landlord and tenant.
    """
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('active', 'Active'),
        ('expiring', 'Expiring Soon'),
        ('expired', 'Expired'),
        ('terminated', 'Terminated'),
    ]

    property = models.ForeignKey(
        'properties.Property',
        on_delete=models.CASCADE,
        related_name='leases'
    )
    unit = models.ForeignKey(
        'properties.Unit',
        on_delete=models.CASCADE,
        related_name='leases'
    )
    tenant = models.ForeignKey(
        'accounts.User',
        on_delete=models.CASCADE,
        related_name='leases',
        limit_choices_to={'is_tenant': True}
    )
    
    # Terms
    start_date = models.DateField()
    end_date = models.DateField()
    monthly_rent = models.DecimalField(
        max_digits=12, 
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    deposit_amount = models.DecimalField(
        max_digits=12, 
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    deposit_paid = models.DecimalField(
        max_digits=12, 
        decimal_places=2, 
        default=0
    )
    
    # Status
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='draft'
    )
    auto_renew = models.BooleanField(default=False)
    
    # Documents
    signed_contract_url = models.URLField(blank=True)

    class Meta:
        db_table = 'tenants_lease'
        ordering = ['-created_at']

    def __str__(self):
        return f"Lease: {self.tenant} - {self.unit}"


class LeaseDocument(TimestampedModel):
    """
    Documents attached to a lease.
    """
    lease = models.ForeignKey(
        Lease,
        on_delete=models.CASCADE,
        related_name='documents'
    )
    document_type = models.CharField(
        max_length=50,
        choices=[
            ('contract', 'Rental Contract'),
            ('id_copy', 'ID Copy'),
            ('proof_of_income', 'Proof of Income'),
            ('utility_bill', 'Utility Bill'),
            ('other', 'Other'),
        ]
    )
    file = models.FileField(upload_to='leases/%Y/%m/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'tenants_lease_document'

    def __str__(self):
        return f"{self.document_type} for {self.lease}"


class TenantUnit(TimestampedModel):
    """
    Current occupancy mapping between tenant and unit.
    """
    tenant = models.ForeignKey(
        'accounts.User',
        on_delete=models.CASCADE,
        related_name='occupied_units'
    )
    unit = models.OneToOneField(
        'properties.Unit',
        on_delete=models.CASCADE,
        related_name='current_tenant'
    )
    lease = models.ForeignKey(
        Lease,
        on_delete=models.CASCADE,
        related_name='tenant_units'
    )
    move_in_date = models.DateField()
    move_out_date = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'tenants_tenant_unit'

    def __str__(self):
        return f"{self.tenant} in {self.unit}"


class MoveInChecklist(TimestampedModel):
    """
    Inspection records during move-in/move-out.
    """
    tenant_unit = models.ForeignKey(
        TenantUnit,
        on_delete=models.CASCADE,
        related_name='checklists'
    )
    item_name = models.CharField(max_length=255)
    condition = models.CharField(
        max_length=50,
        choices=[
            ('excellent', 'Excellent'),
            ('good', 'Good'),
            ('fair', 'Fair'),
            ('poor', 'Poor'),
            ('damaged', 'Damaged'),
        ]
    )
    photo = models.ImageField(
        upload_to='checklists/%Y/%m/', 
        blank=True
    )
    notes = models.TextField(blank=True)
    checked_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'tenants_move_in_checklist'

    def __str__(self):
        return f"{self.item_name} - {self.condition}"
