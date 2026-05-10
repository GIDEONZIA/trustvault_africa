from django.urls import path
from . import views

app_name = 'public_listings'

urlpatterns = [
    path('', views.ListingListView.as_view(), name='listing_list'),
    path('<int:pk>/', views.ListingDetailView.as_view(), name='listing_detail'),
    path('<int:pk>/inquire/', views.InquiryCreateView.as_view(), name='inquiry_create'),
]
