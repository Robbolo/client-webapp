# Generated by Django 5.2 on 2025-04-20 07:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0019_client_completed_sessions_count_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='notification_priority',
            field=models.CharField(choices=[('Reminder', 'Reminder'), ('Urgent', 'Urgent')], default='Reminder', max_length=40),
        ),
        migrations.AddField(
            model_name='notification',
            name='notification_type',
            field=models.CharField(choices=[('Contact', 'Contact'), ('Sessions', 'Sessions'), ('Payment', 'Payment'), ('Other', 'Other')], default='Other', max_length=40),
        ),
    ]
