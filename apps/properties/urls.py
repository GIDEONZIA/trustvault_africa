from django.urls import path

from . import views

app_name = 'properties'

urlpatterns = [
    path('', views.PropertyListView.as_view(), name='list'),
    path('add/', views.PropertyCreateView.as_view(), name='create'),
    path('<slug:slug>/', views.PropertyDetailView.as_view(), name='detail'),
    path('<slug:slug>/edit/', views.PropertyUpdateView.as_view(), name='update'),
    path('<slug:slug>/delete/', views.property_delete, name='delete'),
    path('<slug:property_slug>/units/add/', views.unit_create, name='unit-create'),
    path('units/<int:pk>/edit/', views.unit_update, name='unit-update'),
    path('units/<int:pk>/delete/', views.unit_delete, name='unit-delete'),
]
