from django import forms
from .models import Client, Session

class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = [
            'name',
            'email',
            'phone_number',
            'location',
            'timezone',
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
            'last_contact_date': forms.DateInput(attrs={'type': 'date'}),
            'notes': forms.Textarea(attrs={'rows': 4}),
        }

class SessionForm(forms.ModelForm):
    class Meta:
        model = Session
        fields = ['date', 'session_type', 'topic', 'notes', 'is_completed']
        widgets = {
            'date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'notes': forms.Textarea(attrs={'rows': 4}),
        }