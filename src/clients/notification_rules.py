from datetime import timedelta
from django.utils import timezone
from clients.models import Client, Notification

def should_create_notification(client, message, cooldown_days=7):
    recent_cutoff = timezone.now() - timedelta(days=cooldown_days)
    return not Notification.objects.filter(
        client=client,
        message=message,
        created_at__gte=recent_cutoff
    ).exists()

def notify_clients_not_contacted_weekly():
    month_threshold = timezone.now() - timedelta(days=7)
    clients = Client.objects.filter(last_contact_date__lte=month_threshold)

    for client in clients:
            week_days=7
            message=f"Urgent: It's been a week since you last contacted {client.name}."
            if should_create_notification(client, message, cooldown_days=week_days):
                Notification.objects.create(
                    client=client,
                    message=message,
                    notification_type='Contact',
                    notification_priority='Reminder'
                    )

def notify_clients_not_contacted_monthly():
    month_threshold = timezone.now() - timedelta(days=30)
    clients = Client.objects.filter(last_contact_date__lte=month_threshold)

    for client in clients:
            month_days=30
            message=f"Urgent: It's been {month_days} days since you last contacted {client.name}."
            if should_create_notification(client, message, cooldown_days=month_days):
                Notification.objects.create(
                    client=client,
                    message=message,
                    notification_type='Contact',
                    notification_priority='Reminder'
                    )
                
def notify_clients_low_sessions():
    clients = Client.objects.filter(paid_sessions_remaining=1,
                                    client_status='Paying',
                                    client_lifecycle='Active',
                                    )   

    for client in clients:
        message=f"Reminder: {client.name} has only 1 paid session remaining."
        if should_create_notification(client, message):
             Notification.objects.create(
                client=client,
                message=message,
                notification_type='Sessions',
                notification_priority='Reminder'
                )

def notify_clients_no_sessions_left():
    clients = Client.objects.filter(paid_sessions_remaining=0,
                                    client_status='Paying',
                                    client_lifecycle='Active',
                                    )

    for client in clients:
        message=f"Urgent: {client.name} has no paid sessions remaining."
        if should_create_notification(client, message):
             Notification.objects.create(
                client=client,
                message=message,
                notification_type='Contact',
                notification_priority='Urgent'
                )