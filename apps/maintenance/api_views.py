from django.utils import timezone
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import MaintenanceRequest
from .serializers import MaintenanceRequestSerializer


class MaintenanceListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = MaintenanceRequestSerializer
    filterset_fields = ['status', 'category', 'priority']

    def get_queryset(self):
        user = self.request.user
        if user.is_landlord:
            return MaintenanceRequest.objects.filter(
                unit__building__owner=user
            ).select_related('unit', 'unit__building', 'tenant', 'assigned_to')
        return MaintenanceRequest.objects.filter(tenant=user)

    def perform_create(self, serializer):
        user = self.request.user
        active_lease = user.leases.filter(status='active').first()
        unit = active_lease.unit if active_lease else None
        serializer.save(tenant=user, unit=unit)


class MaintenanceDetailAPIView(generics.RetrieveUpdateAPIView):
    serializer_class = MaintenanceRequestSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_landlord:
            return MaintenanceRequest.objects.filter(unit__building__owner=user)
        return MaintenanceRequest.objects.filter(tenant=user)


class MaintenanceCompleteAPIView(APIView):
    def post(self, request, pk):
        try:
            mr = MaintenanceRequest.objects.get(pk=pk, unit__building__owner=request.user)
        except MaintenanceRequest.DoesNotExist:
            return Response({'success': False, 'message': 'Not found'}, status=404)

        mr.status = 'completed'
        mr.completed_at = timezone.now()
        mr.actual_cost = request.data.get('actual_cost', mr.cost_estimate)
        mr.save()

        return Response({
            'success': True,
            'data': MaintenanceRequestSerializer(mr).data,
            'message': 'Request marked as completed',
        })


class MaintenanceFeedbackAPIView(APIView):
    def post(self, request, pk):
        try:
            mr = MaintenanceRequest.objects.get(pk=pk, tenant=request.user, status='completed')
        except MaintenanceRequest.DoesNotExist:
            return Response({'success': False, 'message': 'Not found'}, status=404)

        mr.tenant_rating = request.data.get('rating')
        mr.tenant_feedback = request.data.get('feedback', '')
        mr.save()

        return Response({
            'success': True,
            'message': 'Feedback submitted',
        })
