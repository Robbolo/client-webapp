from django.shortcuts import render, get_object_or_404, redirect
from ..models import Client
from ..forms import ClientForm
from django.utils import timezone
from clients.notification_engine import run_all_notification_checks

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
    run_all_notification_checks()
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
            print("Form errors:", form.errors) 
    else:
        form = ClientForm(instance=client)


    return render(request, 'clients/edit_client.html', {'form': form, 'client': client})


def update_last_contacted(request, client_id):
    client = get_object_or_404(Client, id=client_id)
    client.last_contact_date = timezone.now().date()
    client.save()
    return redirect('client_detail', client_id=client.id)