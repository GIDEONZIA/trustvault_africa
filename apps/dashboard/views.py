from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q, Sum
from django.shortcuts import render
from django.utils import timezone

from apps.invoices.models import Invoice
from apps.maintenance.models import MaintenanceRequest
from apps.payments.models import Payment
from apps.properties.models import Property
from apps.tenants.models import Lease


@login_required
def dashboard_index(request):
    user = request.user
    if not user.is_landlord:
        from django.shortcuts import redirect
        return redirect('tenants:portal')

    properties = Property.objects.filter(owner=user, is_active=True).prefetch_related('units')
    total_properties = properties.count()
    total_units = sum(p.total_units for p in properties)
    occupied_units = sum(p.occupied_units for p in properties)
    vacant_units = total_units - occupied_units
    occupancy_rate = round((occupied_units / total_units * 100), 1) if total_units > 0 else 0

    now = timezone.now()
    current_month_start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)

    active_leases = Lease.objects.filter(unit__building__owner=user, status='active')
    monthly_rental_income = sum(l.monthly_rent for l in active_leases)

    collected = Payment.objects.filter(
        invoice__lease__unit__building__owner=user,
        status='completed',
        processed_at__gte=current_month_start,
    ).aggregate(total=Sum('amount'))['total'] or 0

    collection_rate = round((float(collected) / float(monthly_rental_income) * 100), 1) if monthly_rental_income > 0 else 0

    outstanding = Invoice.objects.filter(
        lease__unit__building__owner=user,
        status__in=['pending', 'partially_paid', 'overdue'],
    ).aggregate(total=Sum('amount') - Sum('amount_paid'))['total'] or 0

    overdue = Invoice.objects.filter(
        lease__unit__building__owner=user,
        status='overdue',
    ).aggregate(total=Sum('amount') - Sum('amount_paid'))['total'] or 0

    maintenance_costs = MaintenanceRequest.objects.filter(
        unit__building__owner=user,
        completed_at__gte=current_month_start,
        actual_cost__isnull=False,
    ).aggregate(total=Sum('actual_cost'))['total'] or 0

    recent_payments = Payment.objects.filter(
        invoice__lease__unit__building__owner=user,
        status='completed',
    ).select_related('tenant', 'invoice').order_by('-processed_at')[:5]

    recent_maintenance = MaintenanceRequest.objects.filter(
        unit__building__owner=user,
    ).select_related('tenant', 'unit', 'unit__building').order_by('-created_at')[:5]

    expiring_leases = Lease.objects.filter(
        unit__building__owner=user,
        status='active',
        end_date__lte=now.date() + timezone.timedelta(days=30),
        end_date__gte=now.date(),
    ).select_related('tenant', 'unit', 'unit__building')

    overdue_invoices = Invoice.objects.filter(
        lease__unit__building__owner=user,
        status='overdue',
    ).select_related('lease', 'lease__tenant', 'lease__unit')[:5]

    context = {
        'total_properties': total_properties,
        'total_units': total_units,
        'occupied_units': occupied_units,
        'vacant_units': vacant_units,
        'occupancy_rate': occupancy_rate,
        'monthly_rental_income': monthly_rental_income,
        'collected': collected,
        'collection_rate': collection_rate,
        'outstanding': outstanding,
        'overdue': overdue,
        'maintenance_costs': maintenance_costs,
        'net_income': float(collected) - float(maintenance_costs),
        'recent_payments': recent_payments,
        'recent_maintenance': recent_maintenance,
        'expiring_leases': expiring_leases,
        'overdue_invoices': overdue_invoices,
        'properties': properties,
    }
    return render(request, 'dashboard/index.html', context)
