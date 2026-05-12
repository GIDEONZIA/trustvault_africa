from django.urls import path
from . import views

app_name = 'tenants'

urlpatterns = [
    path('leases/', views.LeaseListView.as_view(), name='lease_list'),
    path('leases/create/', views.LeaseCreateView.as_view(), name='lease_form'), # Add this line
    path('leases/<int:pk>/', views.LeaseDetailView.as_view(), name='lease_detail'),
]
