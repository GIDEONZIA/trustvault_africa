from django.urls import path

from . import api_views

urlpatterns = [
    path('payments/initiate/', api_views.PaymentInitiateAPIView.as_view(), name='api-payment-initiate'),
    path('payments/callback/', api_views.MpesaCallbackAPIView.as_view(), name='api-mpesa-callback'),
    path('payments/<int:pk>/status/', api_views.PaymentStatusAPIView.as_view(), name='api-payment-status'),
    path('payments/', api_views.PaymentListAPIView.as_view(), name='api-payments'),
]
