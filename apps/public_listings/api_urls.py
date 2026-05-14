from django.urls import path

from . import api_views

urlpatterns = [
    path('listings/', api_views.PublicListingAPIView.as_view(), name='api-listings'),
    path('listings/<int:pk>/', api_views.PublicListingDetailAPIView.as_view(), name='api-listing-detail'),
]
