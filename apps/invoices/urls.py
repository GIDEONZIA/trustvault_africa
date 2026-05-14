from django.urls import path

from . import views

app_name = 'invoices'

urlpatterns = [
    path('', views.InvoiceListView.as_view(), name='list'),
    path('add/', views.invoice_create, name='create'),
    path('<int:pk>/', views.InvoiceDetailView.as_view(), name='detail'),
    path('<int:pk>/remind/', views.invoice_send_reminder, name='send-reminder'),
    path('<int:pk>/waive/', views.invoice_waive, name='waive'),
]
