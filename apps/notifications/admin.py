from django.contrib import admin
from .models import Notification

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('recipient', 'title', 'channel', 'status', 'created_at')
    list_filter = ('status', 'channel', 'notification_type')
    search_fields = ('recipient__email', 'title', 'message')
    readonly_fields = ('created_at',)
