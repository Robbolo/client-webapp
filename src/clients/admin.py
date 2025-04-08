from django.contrib import admin
from .models import Client, Notification

# Register your models here.
@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'timezone', 'next_session_date', 'client_status', 'frequency', 'payment_tier', 'paypal_link', 'last_contact_date')
    list_filter = ('next_session_date', 'client_status', 'payment_tier', 'timezone', 'frequency')
    search_fields = ('name', 'email', 'location')

admin.site.register(Notification)