from django.contrib import admin
from .models import Subscription

@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('landlord', 'plan_type', 'status', 'current_period_end', 'amount')
    list_filter = ('plan_type', 'status', 'billing_cycle')
    search_fields = ('landlord__email', 'mpesa_phone')
