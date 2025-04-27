from django.shortcuts import render, get_object_or_404, redirect
from ..models import Client, ClientDocument, Invoice
from ..forms import ClientDocumentForm, RenameDocumentForm,AssignPackageForm
from datetime import timedelta
from django.utils import timezone
from django.views.decorators.http import require_POST
from django.core.files import File
from django.conf import settings
from io import BytesIO
from pathlib import Path
from ..utils import generate_invoice_pdf 

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
            client.client_status = 'Paying'
            client.total_revenue += total_price
            client.save()

            # add invoice record
            Invoice.objects.create(
                client=client,
                amount=total_price,
                invoice_date=timezone.now(),
                description=f"{client.name} - {sessions} sessions - £{total_price} - {timezone.now().strftime('%Y-%m-%d')}",
            )

            # Generate PDF invoice
            buffer = BytesIO()
            generate_invoice_pdf(
                buffer=buffer,
                client_name=client.name,
                client_email=client.email,
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