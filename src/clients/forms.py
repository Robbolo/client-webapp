from django import forms
from .models import Client, Session, ClientDocument

class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = [
            'name',
            'email',
            'social_media',
            'location',
            'timezone',
            'client_source',
            'client_status',
            'current_package',
            'paid_sessions_remaining',
            'frequency',
            'payment_info',
            'last_contact_date',
            'notes',
            'photo',
            'price',
            'invoice_status',
            'completed_sessions_count',
            'no_show_sessions_count',
            'client_lifecycle',
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
            'topic': forms.TextInput(attrs={'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'session_type': forms.Select(attrs={'class': 'form-control'}),
        }

class ClientDocumentForm(forms.ModelForm):
    class Meta:
        model = ClientDocument
        fields = ['file', 'description']
        widgets = {
            'description': forms.TextInput(attrs={'class': 'form-control'}),
        }

class RenameDocumentForm(forms.ModelForm):
    class Meta:
        model = ClientDocument
        fields = ['description']
        widgets = {
            'description': forms.TextInput(attrs={'class': 'form-control'})
        }

class AssignPackageForm(forms.Form):
    number_of_sessions = forms.IntegerField(
        min_value=1,
        label="Number of Sessions"
    )
    
    def __init__(self, *args, **kwargs):
        self.client = kwargs.pop('client', None)
        super().__init__(*args, **kwargs)
        if self.client:
            self.price = self.client.price


class EditSessionForm(forms.ModelForm):
    class Meta:
        model = Session
        fields = ['date', 'session_type', 'topic', 'notes']
        widgets = {
            'date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'topic': forms.TextInput(attrs={'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'session_type': forms.Select(attrs={'class': 'form-control'}),
        }