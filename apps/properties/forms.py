from django import forms

from .models import Property, Unit


class PropertyForm(forms.ModelForm):
    class Meta:
        model = Property
        fields = [
            'name', 'property_type', 'address', 'city', 'county',
            'postal_code', 'description', 'year_built', 'rules',
            'cover_photo', 'is_listed',
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-input'}),
            'property_type': forms.Select(attrs={'class': 'form-select'}),
            'address': forms.Textarea(attrs={'class': 'form-input', 'rows': 2}),
            'city': forms.TextInput(attrs={'class': 'form-input'}),
            'county': forms.TextInput(attrs={'class': 'form-input'}),
            'postal_code': forms.TextInput(attrs={'class': 'form-input'}),
            'description': forms.Textarea(attrs={'class': 'form-input', 'rows': 3}),
            'year_built': forms.NumberInput(attrs={'class': 'form-input'}),
            'rules': forms.Textarea(attrs={'class': 'form-input', 'rows': 3}),
        }


class UnitForm(forms.ModelForm):
    class Meta:
        model = Unit
        fields = [
            'unit_number', 'unit_type', 'bedrooms', 'bathrooms',
            'square_footage', 'floor_number', 'is_furnished',
            'monthly_rent', 'deposit_amount', 'deposit_terms',
            'listing_title', 'listing_description', 'is_published',
        ]
        widgets = {
            'unit_number': forms.TextInput(attrs={'class': 'form-input'}),
            'unit_type': forms.Select(attrs={'class': 'form-select'}),
            'bedrooms': forms.NumberInput(attrs={'class': 'form-input'}),
            'bathrooms': forms.NumberInput(attrs={'class': 'form-input'}),
            'square_footage': forms.NumberInput(attrs={'class': 'form-input'}),
            'floor_number': forms.NumberInput(attrs={'class': 'form-input'}),
            'monthly_rent': forms.NumberInput(attrs={'class': 'form-input'}),
            'deposit_amount': forms.NumberInput(attrs={'class': 'form-input'}),
            'deposit_terms': forms.Textarea(attrs={'class': 'form-input', 'rows': 2}),
            'listing_title': forms.TextInput(attrs={'class': 'form-input'}),
            'listing_description': forms.Textarea(attrs={'class': 'form-input', 'rows': 3}),
        }
