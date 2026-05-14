from django import forms

from apps.accounts.models import User

from .models import Lease, TenantProfile


class LeaseForm(forms.ModelForm):
    tenant_email = forms.EmailField(
        required=False,
        widget=forms.EmailInput(attrs={'class': 'form-input', 'placeholder': 'Existing tenant email'}),
        help_text='Enter email of an existing tenant, or fill in new tenant details below.',
    )
    new_tenant_first_name = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-input'}))
    new_tenant_last_name = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-input'}))
    new_tenant_email = forms.EmailField(required=False, widget=forms.EmailInput(attrs={'class': 'form-input'}))
    new_tenant_phone = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-input'}))

    class Meta:
        model = Lease
        fields = [
            'unit', 'start_date', 'end_date', 'monthly_rent',
            'payment_day', 'is_renewable', 'auto_renew', 'lease_document',
        ]
        widgets = {
            'unit': forms.Select(attrs={'class': 'form-select'}),
            'start_date': forms.DateInput(attrs={'class': 'form-input', 'type': 'date'}),
            'end_date': forms.DateInput(attrs={'class': 'form-input', 'type': 'date'}),
            'monthly_rent': forms.NumberInput(attrs={'class': 'form-input'}),
            'payment_day': forms.NumberInput(attrs={'class': 'form-input', 'min': 1, 'max': 28}),
        }

    def clean(self):
        cleaned_data = super().clean()
        tenant_email = cleaned_data.get('tenant_email')
        new_email = cleaned_data.get('new_tenant_email')
        if not tenant_email and not new_email:
            raise forms.ValidationError('Provide an existing tenant email or new tenant details.')
        return cleaned_data

    def save(self, commit=True):
        lease = super().save(commit=False)
        tenant_email = self.cleaned_data.get('tenant_email')
        if tenant_email:
            lease.tenant = User.objects.get(email=tenant_email)
        else:
            tenant = User.objects.create_user(
                email=self.cleaned_data['new_tenant_email'],
                password=User.objects.make_random_password(),
                first_name=self.cleaned_data['new_tenant_first_name'],
                last_name=self.cleaned_data['new_tenant_last_name'],
                phone_number=self.cleaned_data.get('new_tenant_phone', ''),
                user_type='tenant',
            )
            lease.tenant = tenant
        if commit:
            lease.save()
            lease.unit.is_available = False
            lease.unit.save()
        return lease


class TenantProfileForm(forms.ModelForm):
    class Meta:
        model = TenantProfile
        exclude = ['user', 'tenant_score', 'payment_history_score']
        widgets = {
            'employer_name': forms.TextInput(attrs={'class': 'form-input'}),
            'employer_address': forms.Textarea(attrs={'class': 'form-input', 'rows': 2}),
            'job_title': forms.TextInput(attrs={'class': 'form-input'}),
            'monthly_income': forms.NumberInput(attrs={'class': 'form-input'}),
            'employment_type': forms.Select(attrs={'class': 'form-select'}),
            'emergency_contact_name': forms.TextInput(attrs={'class': 'form-input'}),
            'emergency_contact_phone': forms.TextInput(attrs={'class': 'form-input'}),
            'referee_name': forms.TextInput(attrs={'class': 'form-input'}),
            'referee_phone': forms.TextInput(attrs={'class': 'form-input'}),
        }
