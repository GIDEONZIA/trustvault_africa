from rest_framework import serializers

from apps.accounts.serializers import UserMinimalSerializer
from apps.properties.serializers import UnitSerializer

from .models import Lease, TenantProfile


class LeaseSerializer(serializers.ModelSerializer):
    tenant = UserMinimalSerializer(read_only=True)
    unit_detail = UnitSerializer(source='unit', read_only=True)
    days_until_expiry = serializers.IntegerField(read_only=True)
    outstanding_balance = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)

    class Meta:
        model = Lease
        fields = [
            'id', 'lease_number', 'unit', 'unit_detail', 'tenant',
            'start_date', 'end_date', 'monthly_rent', 'payment_day',
            'deposit_paid', 'deposit_status', 'status', 'is_renewable',
            'auto_renew', 'days_until_expiry', 'outstanding_balance',
            'created_at',
        ]
        read_only_fields = ['id', 'lease_number', 'created_at']


class LeaseCreateSerializer(serializers.ModelSerializer):
    tenant_email = serializers.EmailField(required=False)

    class Meta:
        model = Lease
        fields = [
            'unit', 'tenant_email', 'start_date', 'end_date',
            'monthly_rent', 'payment_day', 'is_renewable', 'auto_renew',
        ]


class TenantProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = TenantProfile
        exclude = ['user']
