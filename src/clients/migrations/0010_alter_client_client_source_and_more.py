# Generated by Django 5.2 on 2025-04-12 07:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0009_alter_client_payment_tier'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='client_source',
            field=models.CharField(choices=[('Instagram', 'Instagram'), ('Facebook', 'Facebook'), ('Referral', 'Referral'), ('Website', 'Website'), ('Other', 'Other')], default='Other', max_length=50),
        ),
        migrations.AlterField(
            model_name='client',
            name='client_status',
            field=models.CharField(choices=[('Enquiring', 'Enquiring'), ('Vibe-Check Booked', 'Vibe-Check Booked'), ('Post-Vibe', 'Post-Vibe'), ('Paying', 'Paying')], default='Enquiring', max_length=50),
        ),
        migrations.AlterField(
            model_name='client',
            name='frequency',
            field=models.CharField(choices=[('Weekly', 'Weekly'), ('Fornightly', 'Fortnightly'), ('Monthly', 'Monthly'), ('Ad-hoc', 'Ad-hoc'), ('Paused', 'Paused')], default='Ad-hoc', max_length=50),
        ),
        migrations.AlterField(
            model_name='client',
            name='payment_tier',
            field=models.CharField(choices=[('Free', 'Free'), ('Three-session package', 'Three-session package'), ('Six-session package', 'Six-session package')], default='Free', max_length=50),
        ),
        migrations.AlterField(
            model_name='session',
            name='session_type',
            field=models.CharField(choices=[('Free', 'Free'), ('Lightning', 'Lightning'), ('Package', 'Package')], max_length=50),
        ),
    ]
