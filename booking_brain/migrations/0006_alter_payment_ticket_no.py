# Generated by Django 4.2.5 on 2023-09-26 12:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking_brain', '0005_rename_readyforbooking_passenger_booked_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='Ticket_no',
            field=models.CharField(max_length=50, null=True),
        ),
    ]
