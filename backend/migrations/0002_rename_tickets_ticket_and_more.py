# Generated by Django 4.2 on 2023-04-07 13:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Tickets',
            new_name='Ticket',
        ),
        migrations.RenameField(
            model_name='ticket',
            old_name='ticket_owner',
            new_name='name',
        ),
    ]