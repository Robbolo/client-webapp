from django import forms
from .models import Client

class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = [
            'name',
            'email',
            'phone_number',
            'location',
            'timezone',
            'next_session_date',
            'client_source',
            'client_status',
            'payment_tier',
            'frequency',
            'paypal_link',
            'last_contact_date',
            'notes',
            'photo',
        ]
        widgets = {
            'next_session_date': forms.DateInput(attrs={'type': 'date'}),
            'last_contact_date': forms.DateInput(attrs={'type': 'date'}),
            'notes': forms.Textarea(attrs={'rows': 4}),
        }