from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.accounts.models import User

from .models import Lease
from .serializers import LeaseCreateSerializer, LeaseSerializer


class LeaseListCreateAPIView(generics.ListCreateAPIView):
    filterset_fields = ['status']
    search_fields = ['lease_number', 'tenant__first_name', 'tenant__email']

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return LeaseCreateSerializer
        return LeaseSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_landlord:
            return Lease.objects.filter(
                unit__building__owner=user
            ).select_related('unit', 'unit__building', 'tenant')
        return Lease.objects.filter(tenant=user).select_related('unit', 'unit__building')

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        tenant_email = data.pop('tenant_email', None)
        if tenant_email:
            try:
                tenant = User.objects.get(email=tenant_email, user_type='tenant')
            except User.DoesNotExist:
                return Response({
                    'success': False,
                    'message': 'Tenant not found',
                }, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({
                'success': False,
                'message': 'Tenant email required',
            }, status=status.HTTP_400_BAD_REQUEST)

        lease = Lease.objects.create(tenant=tenant, **data)
        lease.unit.is_available = False
        lease.unit.save()

        return Response({
            'success': True,
            'data': LeaseSerializer(lease).data,
            'message': 'Lease created. First invoice generated.',
        }, status=status.HTTP_201_CREATED)


class LeaseDetailAPIView(generics.RetrieveUpdateAPIView):
    serializer_class = LeaseSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_landlord:
            return Lease.objects.filter(unit__building__owner=user)
        return Lease.objects.filter(tenant=user)


class LeaseTerminateAPIView(APIView):
    def post(self, request, pk):
        try:
            lease = Lease.objects.get(pk=pk, unit__building__owner=request.user, status='active')
        except Lease.DoesNotExist:
            return Response({'success': False, 'message': 'Lease not found'}, status=404)

        lease.status = 'terminated'
        lease.termination_reason = request.data.get('termination_reason', '')
        lease.save()
        lease.unit.is_available = True
        lease.unit.save()
        return Response({
            'success': True,
            'data': LeaseSerializer(lease).data,
            'message': 'Lease terminated',
        })


class LeaseRenewAPIView(APIView):
    def post(self, request, pk):
        try:
            lease = Lease.objects.get(pk=pk, unit__building__owner=request.user)
        except Lease.DoesNotExist:
            return Response({'success': False, 'message': 'Lease not found'}, status=404)

        new_end = request.data.get('new_end_date')
        new_rent = request.data.get('new_monthly_rent', lease.monthly_rent)
        if not new_end:
            return Response({'success': False, 'message': 'new_end_date required'}, status=400)

        lease.status = 'renewed'
        lease.save()

        new_lease = Lease.objects.create(
            unit=lease.unit,
            tenant=lease.tenant,
            start_date=lease.end_date,
            end_date=new_end,
            monthly_rent=new_rent,
            payment_day=lease.payment_day,
            deposit_paid=lease.deposit_paid,
            deposit_status=lease.deposit_status,
            status='active',
        )
        return Response({
            'success': True,
            'data': LeaseSerializer(new_lease).data,
            'message': 'Lease renewed',
        })
