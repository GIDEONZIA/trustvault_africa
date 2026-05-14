from django.urls import path

from . import views

app_name = 'tenants'

urlpatterns = [
    path('leases/', views.LeaseListView.as_view(), name='lease-list'),
    path('leases/add/', views.lease_create, name='lease-create'),
    path('leases/<int:pk>/', views.LeaseDetailView.as_view(), name='lease-detail'),
    path('leases/<int:pk>/terminate/', views.lease_terminate, name='lease-terminate'),
    path('portal/', views.tenant_portal, name='portal'),
]
