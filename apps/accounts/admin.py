from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, LandlordProfile, TenantProfile


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ['email', 'first_name', 'last_name', 'is_landlord', 'is_tenant', 'is_active']
    list_filter = ['is_landlord', 'is_tenant', 'is_active', 'date_joined']
    search_fields = ['email', 'first_name', 'last_name']
    ordering = ['-date_joined']
    
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'phone_number')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Roles', {'fields': ('is_landlord', 'is_tenant', 'is_vendor')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'password1', 'password2'),
        }),
    )


@admin.register(LandlordProfile)
class LandlordProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'phone_number', 'subscription_tier', 'created_at']
    list_filter = ['subscription_tier', 'created_at']
    search_fields = ['user__email', 'user__first_name', 'user__last_name']


@admin.register(TenantProfile)
class TenantProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'phone_number', 'employer_name', 'created_at']
    search_fields = ['user__email', 'user__first_name', 'employer_name']
