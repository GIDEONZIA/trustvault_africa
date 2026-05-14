from django.urls import path

from . import api_views

urlpatterns = [
    path('leases/', api_views.LeaseListCreateAPIView.as_view(), name='api-leases'),
    path('leases/<int:pk>/', api_views.LeaseDetailAPIView.as_view(), name='api-lease-detail'),
    path('leases/<int:pk>/terminate/', api_views.LeaseTerminateAPIView.as_view(), name='api-lease-terminate'),
    path('leases/<int:pk>/renew/', api_views.LeaseRenewAPIView.as_view(), name='api-lease-renew'),
]
