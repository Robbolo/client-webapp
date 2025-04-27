from django.shortcuts import render
from ..models import Client, Session, Invoice
from django.db.models import Count, Sum
from django.db.models.functions import TruncWeek, TruncMonth
from django_tables2 import SingleTableView
from ..tables import ClientTable
import json

class ClientTableView(SingleTableView):
    model = Client
    table_class = ClientTable
    template_name = "clients/client_table.html"

def business_insights(request):
    #add new variable for each new chart
    total_clients = Client.objects.count()
    total_sessions = Session.objects.count()
    session_types = list(Session.objects.values('session_type').annotate(count=Count('id')))
    client_sources = list(Client.objects.values('client_source').annotate(count=Count('id')))
    lifecycle_statuses = list(Client.objects.values('client_lifecycle').annotate(count=Count('id')))
    payment_tiers = list(Client.objects.values('current_package').annotate(count=Count('id')))
    total_revenue = sum(client.total_revenue for client in Client.objects.all())
     ## CHARTS FOR SESSIONS PER WEEK
        # calculate sessions per week for chart
    weekly_sessions = (
        Session.objects.annotate(week=TruncWeek('date'))
        .values('week')
        .annotate(count=Count('id'))
        .order_by('week')
    )
        #turn the sessions per week into json compatible format
    weekly_sessions_data = [
        {"week": entry["week"].strftime('%Y-%m-%d'), "count": entry["count"]}
        for entry in weekly_sessions
    ]
    ## CHARTS FOR CLIENTS PER MONTH
        # calculate clients per month for chart
    monthly_clients = (
        Client.objects.annotate(month=TruncMonth('created_at'))
        .values('month')
        .annotate(count=Count('id'))
        .order_by('month')
    )
        #turn the clients per month into json compatible format
    monthly_clients_data = [
        {"month": entry["month"].strftime('%Y-%m'), "count": entry["count"]}
        for entry in monthly_clients
    ]
    # CHARTS FOR REVENUE PER MONTH
        # calculate revenue per month for chart
    monthly_revenue = (
    Invoice.objects
    .annotate(month=TruncMonth('invoice_date'))
    .values('month')
    .annotate(total=Sum('amount'))
    .order_by('month')
    )
    # turn revnue per month into json compatible format
    monthly_revenue_data = [
        {
        "month": entry["month"].strftime('%Y-%m'),
        "total": float(entry["total"]) if entry["total"] is not None else 0
        }
        for entry in monthly_revenue
]


    #add the new variable to this context dict and json.dumps any non ints
    context = {
        'total_clients': total_clients,
        'client_sources': json.dumps(client_sources),
        'lifecycle_statuses': json.dumps(lifecycle_statuses),
        'payment_tiers': json.dumps(payment_tiers),
        'total_sessions': total_sessions,
        'session_types': json.dumps(session_types),
        'weekly_sessions': json.dumps(weekly_sessions_data),
        'monthly_clients': json.dumps(monthly_clients_data),
        'total_revenue': total_revenue,
        'monthly_revenue': json.dumps(monthly_revenue_data),
    }
    return render(request, 'clients/insights.html', context)