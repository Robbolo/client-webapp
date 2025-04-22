
from django.shortcuts import render
from ..models import Notification
from django.http import HttpResponseRedirect
from django.urls import reverse
from clients.notification_engine import run_all_notification_checks

def notification_dashboard(request):
    run_all_notification_checks()
    notifications = Notification.objects.filter(read=False).order_by('-created_at')
    return render(request, 'clients/notification_dashboard.html', {'notifications': notifications})

# couple with notification dashboard to allow read functionality
def mark_as_read(request, notification_id):
    notification = Notification.objects.get(id=notification_id)
    notification.read = True
    notification.save()
    return HttpResponseRedirect(reverse('notification_dashboard'))

# collate read notifications so they're not lost
def read_notifications(request):
    notifications = Notification.objects.filter(read=True).order_by('-created_at')
    return render(request, 'clients/read_notifications.html', {'notifications': notifications})

