from django.shortcuts import render, get_object_or_404, redirect
from .models import Client, Notification, Session, ClientDocument
from .forms import ClientForm, SessionForm, ClientDocumentForm, RenameDocumentForm,AssignPackageForm
from datetime import timedelta
from django.utils import timezone
from django.http import HttpResponseRedirect, FileResponse
from django.urls import reverse
from django.views.decorators.http import require_POST
from django.core.files import File
from django.conf import settings
from django.db.models import F
from io import BytesIO
from reportlab.pdfgen import canvas
from pathlib import Path
from .utils import generate_invoice_pdf 

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
    client = session.client

    # Mark session complete and not a no-show
    session.is_completed = True
    session.is_no_show = False
    session.save()

    # Increment completed session count (always)
    client.completed_sessions_count = F('completed_sessions_count') + 1

    # Reduce paid session count only for 'package' sessions
    if session.session_type == 'package' and client.paid_sessions_remaining > 0:
        client.paid_sessions_remaining = F('paid_sessions_remaining') - 1

    client.save()
    return redirect('client_detail', client_id=session.client.id)

def mark_session_no_show(request, session_id):
    session = get_object_or_404(Session, pk=session_id)
    client = session.client

    # Mark the session as completed and flagged as a no-show
    session.is_completed = True
    session.is_no_show = True
    session.save()

    # Increment no-show session count (for all session types)
    client.no_show_sessions_count = F('no_show_sessions_count') + 1

    # Reduce paid session count only for package sessions
    if session.session_type == 'package' and client.paid_sessions_remaining > 0:
        client.paid_sessions_remaining = F('paid_sessions_remaining') - 1

    client.save()

    return redirect('client_detail', client_id=client.id)


def undo_session_status(request, session_id):
    session = get_object_or_404(Session, pk=session_id)
    if session.session_type == 'package':
        session.client.paid_sessions_remaining = F('paid_sessions_remaining') + 1
        session.client.save()
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

def upload_document(request, client_id):
    client = get_object_or_404(Client, pk=client_id)

    if request.method == 'POST':
        form = ClientDocumentForm(request.POST, request.FILES)
        if form.is_valid():
            document = form.save(commit=False)
            document.client = client
            document.save()
            return redirect('client_detail', client_id=client.id)
    else:
        form = ClientDocumentForm()

    return render(request, 'clients/upload_document.html', {'form': form, 'client': client})


@require_POST
def delete_document(request, document_id):
    document = get_object_or_404(ClientDocument, id=document_id)
    client_id = document.client.id
    document.file.delete()  # deletes the file from disk
    document.delete()       # deletes the record from DB
    return redirect('client_detail', client_id=client_id)

def rename_document(request, document_id):
    document = get_object_or_404(ClientDocument, id=document_id)
    if request.method == 'POST':
        form = RenameDocumentForm(request.POST, instance=document)
        if form.is_valid():
            form.save()
            return redirect('client_detail', client_id=document.client.id)
    else:
        form = RenameDocumentForm(instance=document)
    
    return render(request, 'clients/rename_document.html', {
        'form': form,
        'document': document
    })

def assign_package(request, client_id):
    client = get_object_or_404(Client, pk=client_id)

    if request.method == 'POST':
        form = AssignPackageForm(request.POST, client=client)
        if form.is_valid():
            sessions = form.cleaned_data['number_of_sessions']
            price = client.price
            total_price = price * sessions

            # Update the client
            client.paid_sessions_remaining += sessions
            client.current_package = f"{sessions}-session package"
            client.last_invoice_date = timezone.now()
            client.invoice_status = 'Generated'
            client.save()

            # Generate PDF invoice
            buffer = BytesIO()
            generate_invoice_pdf(
                buffer=buffer,
                client_name=client.name,
                package_info=f"{sessions} sessions",
                session_price=client.price,
                total_price=total_price,
                due_date=timezone.now().date() + timedelta(days=7),
            )
            buffer.seek(0)


            # Save PDF to media/documents/
            safe_name = client.name.replace(" ", "_").replace("/", "-")
            filename = f"{safe_name}_invoice_{timezone.now().strftime('%Y%m%d_%H%M%S')}.pdf"
            documents_dir = Path(settings.MEDIA_ROOT) / 'documents'
            documents_dir.mkdir(parents=True, exist_ok=True)
            file_path = documents_dir / filename

            with open(file_path, 'wb') as f:
                f.write(buffer.getvalue())

            # Save to ClientDocument model
            with open(file_path, 'rb') as f:
                django_file = File(f)
                document = ClientDocument(
                    client=client,
                    description=filename
                )
                document.file.save(filename, django_file, save=True)

            return redirect('client_detail', client_id=client.id)
    else:
        form = AssignPackageForm(client=client)

    return render(request, 'clients/assign_package.html', {
        'form': form,
        'client': client
    })