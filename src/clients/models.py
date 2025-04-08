from django.db import models


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
            ('USE', 'US East'),
            ('USW', 'US West'),
            ('USC', 'US Central'),
            ('Canada', 'Canada'),
            ('Australia', 'Australia'),
            ('Asia', 'Asia'),
            ('Other', 'Other')
        ],
        default='UK'
        )
    next_session_date = models.DateField(null=True, blank=True)
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
    frequency = models.CharField(
        max_length=50,
        choices=[
            ('weekly', 'Weekly'),
            ('bi-weekly', 'Bi-weekly'),
            ('monthly', 'Monthly'),
            ('adhoc', 'Ad-hoc'),
            ('paused', 'Paused')
            ],
            default='Ad-hoc'
            )
    paypal_link = models.URLField(blank=True)
    last_contact_date = models.DateField(null=True, blank=True)
    notes = models.TextField(blank=True)

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