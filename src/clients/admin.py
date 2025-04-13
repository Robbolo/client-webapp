from django.contrib import admin
from .models import Client, Notification, Session, ClientDocument

# Register your models here.
@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'timezone', 'client_status', 'frequency', 'payment_tier', 'paypal_link', 'last_contact_date')
    list_filter = ('client_status', 'payment_tier', 'timezone', 'frequency')
    search_fields = ('name', 'email', 'location')

admin.site.register(Notification)

@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    list_display = ['client', 'date', 'session_type', 'is_completed', 'is_no_show']
    list_filter = ['is_completed', 'session_type']
    search_fields = ['client__name', 'topic']

@admin.register(ClientDocument)
class ClientDocumentAdmin(admin.ModelAdmin):
    list_display = ['client', 'description', 'file']
    search_fields = ['client__name', 'description']
