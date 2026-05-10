from django.urls import path
from . import views

app_name = 'payments'

urlpatterns = [
    path('history/', views.TransactionListView.as_view(), name='transaction_history'),
    path('stk-push/', views.initiate_stk_push, name='stk_push'),
    path('callback/', views.mpesa_callback, name='mpesa_callback'), # M-Pesa hits this
]
