from django.urls import path
from . import views

app_name = 'tenants'

urlpatterns = [
    path('leases/', views.LeaseListView.as_view(), name='lease_list'),
    path('leases/<int:pk>/', views.LeaseDetailView.as_view(), name='lease_detail'),
]
