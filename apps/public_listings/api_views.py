from rest_framework import generics, permissions

from apps.properties.models import Unit
from apps.properties.serializers import UnitSerializer


class PublicListingAPIView(generics.ListAPIView):
    serializer_class = UnitSerializer
    permission_classes = [permissions.AllowAny]
    filterset_fields = ['unit_type', 'bedrooms']
    search_fields = ['listing_title', 'building__city', 'building__name']

    def get_queryset(self):
        return Unit.objects.filter(
            is_published=True, is_available=True, building__is_active=True,
        ).select_related('building')


class PublicListingDetailAPIView(generics.RetrieveAPIView):
    serializer_class = UnitSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        return Unit.objects.filter(
            is_published=True, is_available=True, building__is_active=True,
        ).select_related('building')
