from django.db.models import Sum
from django.utils import timezone
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.invoices.models import Invoice
from apps.maintenance.models import MaintenanceRequest
from apps.payments.models import Payment
from apps.properties.models import Property
from apps.tenants.models import Lease


class DashboardSummaryAPIView(APIView):
    def get(self, request):
        user = request.user
        properties = Property.objects.filter(owner=user, is_active=True)
        total_units = sum(p.total_units for p in properties)
        occupied = sum(p.occupied_units for p in properties)
        vacant = total_units - occupied

        now = timezone.now()
        month_start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)

        active_leases = Lease.objects.filter(unit__building__owner=user, status='active')
        monthly_income = sum(l.monthly_rent for l in active_leases)

        collected = Payment.objects.filter(
            invoice__lease__unit__building__owner=user,
            status='completed',
            processed_at__gte=month_start,
        ).aggregate(total=Sum('amount'))['total'] or 0

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
            completed_at__gte=month_start,
        ).aggregate(total=Sum('actual_cost'))['total'] or 0

        return Response({
            'success': True,
            'data': {
                'properties_count': properties.count(),
                'total_units': total_units,
                'occupied_units': occupied,
                'vacant_units': vacant,
                'occupancy_rate': round((occupied / total_units * 100), 1) if total_units > 0 else 0,
                'financials': {
                    'monthly_rental_income': float(monthly_income),
                    'collected_this_month': float(collected),
                    'collection_rate': round((float(collected) / float(monthly_income) * 100), 1) if monthly_income else 0,
                    'outstanding_invoices': float(outstanding),
                    'overdue_amount': float(overdue),
                    'maintenance_costs_this_month': float(maintenance_costs),
                    'net_income_this_month': float(collected) - float(maintenance_costs),
                },
            },
        })
