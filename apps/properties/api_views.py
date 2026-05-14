from rest_framework import generics, status
from rest_framework.response import Response

from .models import Property, Unit
from .serializers import PropertyDetailSerializer, PropertySerializer, UnitSerializer


class PropertyListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = PropertySerializer
    filterset_fields = ['property_type', 'is_active', 'city']
    search_fields = ['name', 'address', 'city']

    def get_queryset(self):
        return Property.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response({
            'success': True,
            'data': serializer.data,
            'message': 'Property created successfully',
        }, status=status.HTTP_201_CREATED)


class PropertyDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PropertyDetailSerializer

    def get_queryset(self):
        return Property.objects.filter(owner=self.request.user)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_active = False
        instance.save()
        return Response({
            'success': True,
            'message': 'Property deactivated',
        })


class UnitListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = UnitSerializer
    filterset_fields = ['unit_type', 'is_available']

    def get_queryset(self):
        return Unit.objects.filter(
            building_id=self.kwargs['property_id'],
            building__owner=self.request.user,
        )

    def perform_create(self, serializer):
        prop = Property.objects.get(
            id=self.kwargs['property_id'],
            owner=self.request.user,
        )
        serializer.save(building=prop)


class UnitDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UnitSerializer

    def get_queryset(self):
        return Unit.objects.filter(building__owner=self.request.user)
