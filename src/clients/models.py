from django.db import models
from django.utils import timezone
from django.core.validators import FileExtensionValidator
from pathlib import Path


# Create class for client information
class Client(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20, blank=True)
    location = models.CharField(max_length=100, blank=True)
    timezone = models.CharField(
        max_length=50,
        choices=[
            ('UK', 'UK'),
            ('Europe', 'Europe'),
            ('US East', 'US East'),
            ('US West', 'US West'),
            ('US Central', 'US Central'),
            ('Canada', 'Canada'),
            ('Australia', 'Australia'),
            ('Asia', 'Asia'),
            ('Other', 'Other')
        ],
        default='UK'
        )
    client_source = models.CharField(
        max_length=50,
        choices=[
            ('Instagram', 'Instagram'),
            ('Facebook', 'Facebook'),
            ('Referral', 'Referral'),
            ('Website', 'Website'),
            ('Other', 'Other')
            ],
            default='Other'

            )
    client_status = models.CharField( 
        max_length=50,
        choices=[
            ('Enquiring', 'Enquiring'),
            ('Vibe-Check Booked', 'Vibe-Check Booked'),
            ('Post-Vibe', 'Post-Vibe'),
            ('Paying', 'Paying')
            ],
            default='Enquiring'
            )
    payment_tier = models.CharField(  
        max_length=50,
        choices=[
            ('Free', 'Free'), 
            ('Three-session package', 'Three-session package'), 
            ('Six-session package', 'Six-session package'),
            ],
            default='Free' 
            )
    frequency = models.CharField(
        max_length=50,
        choices=[
            ('Weekly', 'Weekly'),
            ('Fornightly', 'Fortnightly'),
            ('Monthly', 'Monthly'),
            ('Ad-hoc', 'Ad-hoc'),
            ('Paused', 'Paused')
            ],
            default='Ad-hoc'
            )
    paypal_link = models.URLField(blank=True)
    last_contact_date = models.DateField(null=True, blank=True)
    notes = models.TextField(blank=True)
    photo = models.ImageField(upload_to='client_photos/', blank=True, null=True)

    def __str__(self):
        return self.name
    
# sets up model for notifications     
class Notification(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)

    def __str__(self):
        return f"Notification for {self.client.name}"

    @property
    def is_new(self):
        return not self.read
    
class Session(models.Model):
    client = models.ForeignKey('Client', on_delete=models.CASCADE, related_name='sessions')
    date = models.DateTimeField()
    session_type = models.CharField(
        max_length=50,
        choices=[
            ('Free', 'Free'),
            ('Lightning', 'Lightning'),
            ('Package', 'Package'),
        ])
    topic = models.CharField(max_length=200, blank=True)
    notes = models.TextField(blank=True)
    is_completed = models.BooleanField(default=False)
    is_no_show = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.client.name} - {self.date.strftime('%Y-%m-%d %H:%M')}"
    
    
class ClientDocument(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='documents')
    file = models.FileField(
        upload_to='documents/',
        validators=[FileExtensionValidator(allowed_extensions=['pdf', 'doc', 'docx', 'txt', 'xls', 'xlsx', 'csv'])]
    )
    description = models.CharField(max_length=255, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    @property
    def file_extension(self):
        return Path(self.file.name).suffix.lower()
    
    @property
    def file_size_kb(self):
        return round(self.file.size / 1024, 1)  # returns size in KB

    def __str__(self):
        return f"Document for {self.client.name}: {self.file.name}"