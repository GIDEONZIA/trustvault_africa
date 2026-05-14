from django.urls import path

from . import api_views

urlpatterns = [
    path('properties/', api_views.PropertyListCreateAPIView.as_view(), name='api-properties'),
    path('properties/<int:pk>/', api_views.PropertyDetailAPIView.as_view(), name='api-property-detail'),
    path('properties/<int:property_id>/units/', api_views.UnitListCreateAPIView.as_view(), name='api-units'),
    path('units/<int:pk>/', api_views.UnitDetailAPIView.as_view(), name='api-unit-detail'),
]
