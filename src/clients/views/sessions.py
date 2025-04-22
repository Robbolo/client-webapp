from django.shortcuts import render, get_object_or_404, redirect
from ..models import Client, Session
from ..forms import SessionForm, EditSessionForm
from datetime import timedelta
from django.utils import timezone
from django.db.models import F

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

def edit_session(request, session_id):
    session = get_object_or_404(Session, id=session_id)

    if request.method == 'POST':
        form = EditSessionForm(request.POST, instance=session)
        if form.is_valid():
            form.save()
            return redirect('client_detail', client_id=session.client.id)
    else:
        form = EditSessionForm(instance=session)

    return render(request, 'clients/edit_session.html', {'form': form, 'session': session})