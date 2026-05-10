from django.urls import path
from . import views

app_name = 'maintenance'

urlpatterns = [
    path('request/', views.MaintenanceRequestCreateView.as_view(), name='request_create'),
    path('history/', views.MaintenanceRequestListView.as_view(), name='request_list'),
    path('request/<int:pk>/', views.MaintenanceRequestDetailView.as_view(), name='request_detail'),
]
