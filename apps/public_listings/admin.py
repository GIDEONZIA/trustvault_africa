from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import PublicListing, Inquiry, ViewingSchedule

class ViewingScheduleInline(admin.TabularInline):
    model = ViewingSchedule
    extra = 1

@admin.register(PublicListing)
class PublicListingAdmin(admin.ModelAdmin):
    list_display = ('title', 'unit', 'is_active', 'is_featured', 'view_count', 'created_at')
    list_filter = ('is_active', 'is_featured')
    search_fields = ('title', 'description')
    readonly_fields = ('view_count',)

@admin.register(Inquiry)
class InquiryAdmin(admin.ModelAdmin):
    list_display = ('name', 'listing', 'phone', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('name', 'phone', 'email')
    inlines = [ViewingScheduleInline]

@admin.register(ViewingSchedule)
class ViewingScheduleAdmin(admin.ModelAdmin):
    list_display = ('inquiry', 'scheduled_date', 'scheduled_time', 'status')
    list_filter = ('status', 'scheduled_date')
