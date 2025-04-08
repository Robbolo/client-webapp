from django.shortcuts import render, get_object_or_404
from .models import Client

# Create your views here.
def client_detail(request, client_id):
    client = get_object_or_404(Client, id=client_id)
    return render(request, 'clients/client_detail.html', {'client': client})