from django.urls import path

from . import views

app_name = 'payments'

urlpatterns = [
    path('initiate/<int:invoice_id>/', views.payment_initiate, name='initiate'),
    path('callback/', views.mpesa_callback, name='mpesa-callback'),
    path('<int:pk>/status/', views.payment_status, name='status'),
    path('history/', views.payment_history, name='history'),
    path('record/<int:invoice_id>/', views.record_manual_payment, name='record-manual'),
]
