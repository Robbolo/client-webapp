from django.db import models
import pytz

# Create class for client information
class Client(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20, blank=True)
    location = models.CharField(max_length=100, blank=True)
    timezone = models.CharField(
        max_length=50,
        choices=[(tz, tz) for tz in pytz.common_timezones],  # Dropdown of common timezones
        default='UTC'
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
            default='facebook'
            )
    client_status = models.CharField( 
        max_length=50,
        choices=[
            ('enquiring', 'Enquiring'),
            ('vibe-check booked', 'Vibe-Check Booked'),
            ('post-vibe', 'Post-Vibe'),
            ('paying', 'Paying')
            ],
            default='enquiring'
            )
    payment_tier = models.CharField(  
        max_length=50,
        choices=[
            ('free', 'Free'), 
            ('three-session', 'Three-session package'), 
            ('six-session', 'Six-session package'),
            ],
            default='free' 
            )
    last_contact_date = models.DateField(null=True, blank=True)
    notes = models.TextField(blank=True)

    def __str__(self):
        return self.name