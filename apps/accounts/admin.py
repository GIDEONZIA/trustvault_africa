from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin, GroupAdmin as BaseGroupAdmin
from django.contrib.auth.models import Group, Permission
from .models import User, LandlordProfile, TenantProfile


# Register Permission FIRST (before UserAdmin)
@admin.register(Permission)
class PermissionAdmin(admin.ModelAdmin):
    search_fields = ('name', 'codename')


# Register Group
admin.site.unregister(Group)

@admin.register(Group)
class GroupAdmin(BaseGroupAdmin):
    search_fields = ('name',)


# Inlines
class LandlordProfileInline(admin.StackedInline):
    model = LandlordProfile
    can_delete = False
    verbose_name_plural = "Landlord Profile"


class TenantProfileInline(admin.StackedInline):
    model = TenantProfile
    can_delete = False
    verbose_name_plural = "Tenant Profile"


# UserAdmin LAST (after Permission is registered)
@admin.register(User)
class UserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Personal Info", {"fields": ("first_name", "last_name", "phone_number")}),
        ("Roles", {"fields": ("is_landlord", "is_tenant", "is_vendor")}),
        ("Verification", {"fields": ("email_verified", "phone_verified")}),
        ("Status", {"fields": ("is_active", "is_staff", "is_superuser")}),
        ("Permissions", {"fields": ("groups", "user_permissions")}),
    )
    
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "password1", "password2", "first_name", "last_name"),
        }),
    )
    
    list_display = ("email", "first_name", "last_name", "is_landlord", "is_tenant", "is_staff", "is_active")
    list_filter = ("is_landlord", "is_tenant", "is_staff", "is_active", "email_verified")
    search_fields = ("email", "first_name", "last_name")
    ordering = ("-date_joined",)
    filter_horizontal = ("groups", "user_permissions")
    inlines = (LandlordProfileInline, TenantProfileInline)
    exclude = ("date_joined", "last_login")


@admin.register(LandlordProfile)
class LandlordProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "phone_number", "subscription_tier", "created_at")
    list_filter = ("subscription_tier",)
    search_fields = ("user__email", "user__first_name", "user__last_name", "phone_number")
    readonly_fields = ("created_at",)


@admin.register(TenantProfile)
class TenantProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "phone_number", "monthly_income", "created_at")
    search_fields = ("user__email", "user__first_name", "user__last_name", "phone_number")
    readonly_fields = ("created_at",)