import django_tables2 as tables
from .models import Client

class ClientTable(tables.Table):
    name = tables.Column(linkify=lambda record: f"/client/{record.id}/")
    last_contact_date = tables.DateColumn()
    paid_sessions_remaining = tables.Column()
    client_status = tables.Column()
    client_lifecycle = tables.Column()

    class Meta:
        model = Client
        template_name = "django_tables2/bootstrap4.html"
        fields = ("name",
                  "client_status",
                  "client_lifecycle",
                  "paid_sessions_remaining",
                  "last_contact_date",
                  "invoice_status",
                  "last_invoice_date",
                  )