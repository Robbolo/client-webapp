# Generated by Django 5.2 on 2025-04-15 19:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0016_client_last_invoice_date'),
    ]

    operations = [
        migrations.RenameField(
            model_name='client',
            old_name='phone_number',
            new_name='social_media',
        ),
    ]
