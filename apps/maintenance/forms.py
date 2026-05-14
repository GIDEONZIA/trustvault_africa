from django import forms

from .models import MaintenanceRequest


class MaintenanceRequestForm(forms.ModelForm):
    class Meta:
        model = MaintenanceRequest
        fields = ['title', 'description', 'category', 'priority']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Brief description of the issue'}),
            'description': forms.Textarea(attrs={'class': 'form-input', 'rows': 4, 'placeholder': 'Describe the issue in detail...'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'priority': forms.Select(attrs={'class': 'form-select'}),
        }


class MaintenanceUpdateForm(forms.ModelForm):
    class Meta:
        model = MaintenanceRequest
        fields = ['status', 'assigned_to', 'landlord_notes', 'cost_estimate']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-select'}),
            'assigned_to': forms.Select(attrs={'class': 'form-select'}),
            'landlord_notes': forms.Textarea(attrs={'class': 'form-input', 'rows': 3}),
            'cost_estimate': forms.NumberInput(attrs={'class': 'form-input'}),
        }
