from django.contrib import admin
from .models import Client

# Register your models here.
@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'timezone', 'client_status', 'payment_tier', 'last_contact_date')
    list_filter = ('client_status', 'payment_tier', 'timezone')
    search_fields = ('name', 'email', 'location')