from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import View, TemplateView, UpdateView
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator

from .models import User, LandlordProfile, TenantProfile
from .forms import (
    UserRegistrationForm, 
    UserLoginForm, 
    UserProfileUpdateForm,
    LandlordProfileForm,
    TenantProfileForm
)


class RegisterView(View):
    """Handle user registration with role selection"""
    
    def get(self, request):
        form = UserRegistrationForm()
        return render(request, "accounts/register.html", {"form": form})
    
    def post(self, request):
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            role = form.cleaned_data.get("role")
            
            if role == "landlord":
                user.is_landlord = True
            elif role == "tenant":
                user.is_tenant = True
            elif role == "vendor":
                user.is_vendor = True
            
            user.save()
            
            # Create profile based on role
            if user.is_landlord:
                LandlordProfile.objects.create(user=user, phone_number=user.phone_number or "")
            elif user.is_tenant:
                TenantProfile.objects.create(user=user, phone_number=user.phone_number or "")
            
            login(request, user)
            messages.success(request, "Registration successful!")
            return redirect("accounts:dashboard")
        
        return render(request, "accounts/register.html", {"form": form})


class LoginView(View):
    """Handle user login with email"""
    
    def get(self, request):
        form = UserLoginForm()
        return render(request, "accounts/login.html", {"form": form})
    
    def post(self, request):
        form = UserLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")
            user = authenticate(request, email=email, password=password)
            
            if user is not None:
                login(request, user)
                messages.success(request, f"Welcome back, {user.first_name}!")
                return redirect("accounts:dashboard")
            else:
                messages.error(request, "Invalid email or password.")
        
        return render(request, "accounts/login.html", {"form": form})


class LogoutView(View):
    """Handle user logout"""
    
    def get(self, request):
        logout(request)
        messages.info(request, "You have been logged out.")
        return redirect("accounts:login")


@method_decorator(login_required, name="dispatch")
class DashboardView(TemplateView):
    """Role-based dashboard redirect"""
    
    template_name = "accounts/dashboard.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        
        if user.is_landlord:
            context["profile"] = getattr(user, "landlord_profile", None)
            context["role"] = "Landlord"
        elif user.is_tenant:
            context["profile"] = getattr(user, "tenant_profile", None)
            context["role"] = "Tenant"
        elif user.is_vendor:
            context["role"] = "Vendor"
        else:
            context["role"] = "User"
        
        return context


@method_decorator(login_required, name="dispatch")
class ProfileUpdateView(UpdateView):
    """Update user profile"""
    
    model = User
    form_class = UserProfileUpdateForm
    template_name = "accounts/profile_update.html"
    success_url = reverse_lazy("accounts:dashboard")
    
    def get_object(self):
        return self.request.user
    
    def form_valid(self, form):
        messages.success(self.request, "Profile updated successfully!")
        return super().form_valid(form)


@method_decorator(login_required, name="dispatch")
class LandlordProfileUpdateView(UpdateView):
    """Update landlord-specific profile"""
    
    model = LandlordProfile
    form_class = LandlordProfileForm
    template_name = "accounts/landlord_profile.html"
    success_url = reverse_lazy("accounts:dashboard")
    
    def get_object(self):
        return get_object_or_404(LandlordProfile, user=self.request.user)


@method_decorator(login_required, name="dispatch")
class TenantProfileUpdateView(UpdateView):
    """Update tenant-specific profile"""
    
    model = TenantProfile
    form_class = TenantProfileForm
    template_name = "accounts/tenant_profile.html"
    success_url = reverse_lazy("accounts:dashboard")
    
    def get_object(self):
        return get_object_or_404(TenantProfile, user=self.request.user)