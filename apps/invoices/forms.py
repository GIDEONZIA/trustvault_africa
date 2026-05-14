from django import forms

from .models import Invoice


class InvoiceForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = ['lease', 'invoice_type', 'amount', 'due_date', 'description']
        widgets = {
            'lease': forms.Select(attrs={'class': 'form-select'}),
            'invoice_type': forms.Select(attrs={'class': 'form-select'}),
            'amount': forms.NumberInput(attrs={'class': 'form-input'}),
            'due_date': forms.DateInput(attrs={'class': 'form-input', 'type': 'date'}),
            'description': forms.Textarea(attrs={'class': 'form-input', 'rows': 3}),
        }
