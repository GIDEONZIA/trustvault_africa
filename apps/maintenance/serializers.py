from rest_framework import serializers

from apps.accounts.serializers import UserMinimalSerializer

from .models import MaintenanceRequest


class MaintenanceRequestSerializer(serializers.ModelSerializer):
    tenant = UserMinimalSerializer(read_only=True)
    assigned_to_detail = UserMinimalSerializer(source='assigned_to', read_only=True)
    unit_number = serializers.CharField(source='unit.unit_number', read_only=True)
    property_name = serializers.CharField(source='unit.building.name', read_only=True)
    days_open = serializers.IntegerField(read_only=True)

    class Meta:
        model = MaintenanceRequest
        fields = [
            'id', 'request_number', 'title', 'description', 'category',
            'priority', 'status', 'unit', 'unit_number', 'property_name',
            'tenant', 'assigned_to', 'assigned_to_detail', 'landlord_notes',
            'cost_estimate', 'actual_cost', 'tenant_rating', 'tenant_feedback',
            'photos', 'completion_photos', 'days_open', 'submitted_at',
            'reviewed_at', 'started_at', 'completed_at',
        ]
        read_only_fields = ['id', 'request_number', 'submitted_at']
