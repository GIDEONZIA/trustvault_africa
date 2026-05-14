from django.urls import path

from . import api_views

urlpatterns = [
    path('maintenance/', api_views.MaintenanceListCreateAPIView.as_view(), name='api-maintenance'),
    path('maintenance/<int:pk>/', api_views.MaintenanceDetailAPIView.as_view(), name='api-maintenance-detail'),
    path('maintenance/<int:pk>/complete/', api_views.MaintenanceCompleteAPIView.as_view(), name='api-maintenance-complete'),
    path('maintenance/<int:pk>/feedback/', api_views.MaintenanceFeedbackAPIView.as_view(), name='api-maintenance-feedback'),
]
