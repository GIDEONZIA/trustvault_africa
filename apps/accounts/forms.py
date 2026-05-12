from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, LandlordProfile, TenantProfile


class UserRegistrationForm(UserCreationForm):
    """Registration form with role selection"""
    
    ROLE_CHOICES = [
        ("tenant", "Tenant"),
        ("landlord", "Landlord"),
        ("vendor", "Vendor"),
    ]
    
    first_name = forms.CharField(max_length=150, required=True)
    last_name = forms.CharField(max_length=150, required=True)
    phone_number = forms.CharField(max_length=15, required=False)
    role = forms.ChoiceField(choices=ROLE_CHOICES, initial="tenant")
    
    class Meta:
        model = User
        fields = ("email", "first_name", "last_name", "phone_number", "password1", "password2")
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.phone_number = self.cleaned_data.get("phone_number", "")
        if commit:
            user.save()
        return user


class UserLoginForm(forms.Form):
    """Login form using email"""
    
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)


class UserProfileUpdateForm(forms.ModelForm):
    """Update basic user info"""
    
    class Meta:
        model = User
        fields = ("first_name", "last_name", "phone_number", "email_verified", "phone_verified")


class LandlordProfileForm(forms.ModelForm):
    """Update landlord profile"""
    
    class Meta:
        model = LandlordProfile
        fields = ("phone_number", "id_number", "kra_pin", "bank_name", "bank_account", "subscription_tier")


class TenantProfileForm(forms.ModelForm):
    """Update tenant profile"""
    
    class Meta:
        model = TenantProfile
        fields = ("phone_number", "emergency_name", "emergency_phone", "employer_name", "employer_phone", "monthly_income")