from django.shortcuts import render

# Create your views here.
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Transaction
import json

class TransactionListView(LoginRequiredMixin, ListView):
    model = Transaction
    template_name = 'payments/transaction_list.html'
    context_object_name = 'transactions'

    def get_queryset(self):
        return Transaction.objects.filter(tenant=self.request.user)

@csrf_exempt
def mpesa_callback(request):
    # Log the callback data from Safaricom
    data = json.loads(request.body)
    print(f"M-Pesa Callback Received: {data}")
    # Logic to update MpesaPayment and Transaction status goes here
    return JsonResponse({"ResultCode": 0, "ResultDesc": "Success"})

def initiate_stk_push(request):
    # Logic to call Safaricom API goes here
    return JsonResponse({"status": "Request Sent"})
