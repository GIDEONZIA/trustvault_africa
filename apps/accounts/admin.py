from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, LandlordProfile, TenantProfile

class LandlordProfileInline(admin.StackedInline):
    model = LandlordProfile
    can_delete = False

class TenantProfileInline(admin.StackedInline):
    model = TenantProfile
    can_delete = False

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    # Fieldsets define how the user edit page looks
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'phone_number')}),
        ('Roles', {'fields': ('is_landlord', 'is_tenant', 'is_vendor')}),
        ('Verification', {'fields': ('email_verified', 'phone_verified')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
    )
    list_display = ('email', 'first_name', 'last_name', 'is_landlord', 'is_tenant', 'is_staff')
    list_filter = ('is_landlord', 'is_tenant', 'is_staff', 'is_active')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('-date_joined',)
    inlines = (LandlordProfileInline, TenantProfileInline)

admin.site.register(LandlordProfile)
admin.site.register(TenantProfile)
