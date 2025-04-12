from django.shortcuts import render, get_object_or_404, redirect
from .models import Client, Notification, Session
from .forms import ClientForm, SessionForm
from datetime import timedelta
from django.utils import timezone
from django.http import HttpResponseRedirect
from django.urls import reverse

# Create your views here.
def client_detail(request, client_id):
    client = get_object_or_404(Client, id=client_id)
    # Get the client's sessions
    upcoming_sessions = client.sessions.filter(is_completed=False).order_by('date')
    past_sessions = client.sessions.filter(is_completed=True).order_by('-date')
    return render(request, 'clients/client_detail.html', {'client': client,
                                                          'upcoming_sessions': upcoming_sessions,
                                                          'past_sessions': past_sessions
                                                          })

def client_list(request):
    query = request.GET.get('q', '')  # Get search term from URL query parameter (default empty string)
    
    if query:
        # Filter clients based on name, email, or status
        clients = Client.objects.filter(
            name__icontains=query) | Client.objects.filter(
            email__icontains=query) | Client.objects.filter(
            client_status__icontains=query)
    else:
        clients = Client.objects.all()

    return render(request, 'clients/client_list.html', {'clients': clients, 'query': query})

# function to generate notifications - will get called during the dashboard view
def create_notifications():
    # Get clients who haven't been contacted in the last 7 or 30 days
    week_threshold = timezone.now() - timedelta(days=7)
    month_threshold = timezone.now() - timedelta(days=30)

    # Find clients needing a 1-week notification
    clients_for_weekly_notification = Client.objects.filter(last_contact_date__lte=week_threshold)

    # Find clients needing a 1-month notification
    clients_for_monthly_notification = Client.objects.filter(last_contact_date__lte=month_threshold)

    # Create notifications for each client
    for client in clients_for_weekly_notification:
        Notification.objects.get_or_create(
            client=client,
            message=f"Reminder: It's been a week since you last contacted {client.name}.",
        )
    
    for client in clients_for_monthly_notification:
        Notification.objects.get_or_create(
            client=client,
            message=f"Urgent: It's been a month since you last contacted {client.name}.",
        )

def notification_dashboard(request):
    create_notifications()  # Call the function to generate notifications - move to cronjob
    notifications = Notification.objects.filter(read=False).order_by('-created_at')  # Unread notifications, newest first
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


def add_client(request):
    if request.method == 'POST':
        form = ClientForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('client_list')  # Redirect to the client list view
    else:
        form = ClientForm()
    
    return render(request, 'clients/add_client.html', {'form': form})

def edit_client(request, client_id):
    client = get_object_or_404(Client, id=client_id)

    if request.method == 'POST':
        form = ClientForm(request.POST, request.FILES, instance=client)
        if form.is_valid():
            form.save()
            return redirect('client_detail', client_id=client.id)
    else:
        form = ClientForm(instance=client)

    return render(request, 'clients/edit_client.html', {'form': form, 'client': client})


def add_session(request, client_id):
    client = get_object_or_404(Client, pk=client_id)

    if request.method == 'POST':
        form = SessionForm(request.POST)
        if form.is_valid():
            session = form.save(commit=False)
            session.client = client  # ✅ Link session to the correct client
            session.save()
            return redirect('client_detail', client_id=client.id)
    else:
        form = SessionForm()

    return render(request, 'clients/add_session.html', {'form': form, 'client': client})

def mark_session_completed(request, session_id):
    session = get_object_or_404(Session, pk=session_id)
    session.is_completed = True
    session.is_no_show = False
    session.save()
    return redirect('client_detail', client_id=session.client.id)

def mark_session_no_show(request, session_id):
    session = get_object_or_404(Session, pk=session_id)
    session.is_completed = True
    session.is_no_show = True
    session.save()
    return redirect('client_detail', client_id=session.client.id)


def undo_session_status(request, session_id):
    session = get_object_or_404(Session, pk=session_id)
    session.is_completed = False
    session.is_no_show = False
    session.save()
    return redirect('client_detail', client_id=session.client.id)

def upcoming_sessions(request):
    sessions = Session.objects.filter(is_completed=False).order_by('date')

    today = timezone.localtime(timezone.now()).date()
    tomorrow = today + timedelta(days=1)

    return render(request, 'clients/upcoming_sessions.html', {
        'sessions': sessions,
        'today': today,
        'tomorrow': tomorrow,
    })