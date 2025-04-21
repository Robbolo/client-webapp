from django.db import models
from django.utils import timezone
from django.core.validators import FileExtensionValidator
from pathlib import Path


# Create class for client information
class Client(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    social_media = models.CharField(max_length=20, blank=True)
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
    current_package = models.CharField(  
        max_length=50,
        choices=[
            ('Free', 'Free'), 
            ('3-session package', '3-session package'), 
            ('6-session package', '6-session package'),
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
    payment_info = models.CharField(max_length=50, blank=True)
    last_contact_date = models.DateField(null=True, blank=True)
    notes = models.TextField(blank=True)
    photo = models.ImageField(upload_to='client_photos/', blank=True, null=True)
    price = models.DecimalField(max_digits=5, decimal_places=0, default=80)
    paid_sessions_remaining = models.PositiveIntegerField(default=0)
    last_invoice_date = models.DateField(null=True, blank=True)
    invoice_status = models.CharField(
        max_length=50,
        choices = [
            ('No need', 'No need'),
            ('Generated', 'Generated'),
            ('Sent', 'Sent'),
            ('Paid', 'Paid'),
            ('Issue', 'Issue')
            ],
        default='No need'
        )
    completed_sessions_count = models.PositiveIntegerField(default=0)
    no_show_sessions_count = models.PositiveIntegerField(default=0)
    client_lifecycle = models.CharField(
        max_length=20,
        choices = [
            ('Active', 'Active'),
            ('Paused', 'Paused'),
            ('Inactive', 'Inactive'),
            ('Archived', 'Archived'),
            ],
        default='Active'
        )
    lifecycle_status_date = models.DateField(null=True, blank=True)
    def save(self, *args, **kwargs):
        if self.pk:
            original = Client.objects.get(pk=self.pk)
            if original.client_lifecycle != self.client_lifecycle:
                self.lifecycle_status_date = timezone.now().date()
        else:
            self.lifecycle_status_date = timezone.now().date()

        super().save(*args, **kwargs)

    @property
    def next_session(self):
        return self.sessions.filter(
            is_completed=False,
            date__gte=timezone.now()
        ).order_by('date').first()
    
    def __str__(self):
        return self.name
    
# sets up model for notifications     
class Notification(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)

    notification_types = [('Contact', 'Contact'),
                          ('Sessions', 'Sessions'),
                          ('Payment', 'Payment'),
                          ('Other', 'Other')]
    notification_type = models.CharField(
        max_length=40,
        choices=notification_types,
        default='Other'
        )
    
    priority_levels = [('Reminder', 'Reminder'),
                      ('Urgent', 'Urgent'),
                      ]
    notification_priority = models.CharField(
        max_length=40,
        choices=priority_levels,
        default='Reminder'
        )

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