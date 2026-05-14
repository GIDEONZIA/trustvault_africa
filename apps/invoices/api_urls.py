from django.urls import path

from . import api_views

urlpatterns = [
    path('invoices/', api_views.InvoiceListCreateAPIView.as_view(), name='api-invoices'),
    path('invoices/<int:pk>/', api_views.InvoiceDetailAPIView.as_view(), name='api-invoice-detail'),
    path('invoices/<int:pk>/send-reminder/', api_views.InvoiceSendReminderAPIView.as_view(), name='api-invoice-remind'),
    path('invoices/<int:pk>/waive/', api_views.InvoiceWaiveAPIView.as_view(), name='api-invoice-waive'),
]
