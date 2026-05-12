from django.urls import path
from . import views

app_name = 'properties'

urlpatterns = [
    path('', views.PropertyListView.as_view(), name='property_list'),
    path('create/', views.PropertyCreateView.as_view(), name='property_form'),
    path('<int:pk>/', views.PropertyDetailView.as_view(), name='property_detail'),
    path('units/', views.UnitListView.as_view(), name='unit_list'),
    path('units/create/', views.UnitCreateView.as_view(), name='unit_form'),
    path('units/<int:pk>/', views.UnitDetailView.as_view(), name='unit_detail'),
]
