from rest_framework import serializers

from apps.accounts.serializers import UserMinimalSerializer

from .models import Property, Unit


class UnitSerializer(serializers.ModelSerializer):
    current_tenant = UserMinimalSerializer(read_only=True)

    class Meta:
        model = Unit
        fields = [
            'id', 'unit_number', 'unit_type', 'bedrooms', 'bathrooms',
            'square_footage', 'floor_number', 'is_furnished', 'monthly_rent',
            'deposit_amount', 'deposit_terms', 'unit_amenities', 'photos',
            'is_available', 'available_from', 'listing_title',
            'listing_description', 'is_published', 'current_tenant',
            'created_at',
        ]
        read_only_fields = ['id', 'created_at']


class PropertySerializer(serializers.ModelSerializer):
    total_units = serializers.IntegerField(read_only=True)
    available_units = serializers.IntegerField(read_only=True)
    occupied_units = serializers.IntegerField(read_only=True)
    occupancy_rate = serializers.FloatField(read_only=True)
    monthly_revenue = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)

    class Meta:
        model = Property
        fields = [
            'id', 'name', 'slug', 'address', 'city', 'county', 'postal_code',
            'property_type', 'description', 'amenities', 'year_built',
            'cover_photo', 'is_active', 'is_listed', 'total_units',
            'available_units', 'occupied_units', 'occupancy_rate',
            'monthly_revenue', 'created_at',
        ]
        read_only_fields = ['id', 'slug', 'created_at']


class PropertyDetailSerializer(PropertySerializer):
    units = UnitSerializer(many=True, read_only=True)

    class Meta(PropertySerializer.Meta):
        fields = PropertySerializer.Meta.fields + ['units', 'rules', 'photo_gallery']
