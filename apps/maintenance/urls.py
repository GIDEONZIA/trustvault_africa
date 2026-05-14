from django.urls import path

from . import views

app_name = 'maintenance'

urlpatterns = [
    path('', views.MaintenanceListView.as_view(), name='list'),
    path('submit/', views.maintenance_create, name='create'),
    path('<int:pk>/', views.MaintenanceDetailView.as_view(), name='detail'),
    path('<int:pk>/update/', views.maintenance_update, name='update'),
    path('<int:pk>/feedback/', views.maintenance_feedback, name='feedback'),
]
