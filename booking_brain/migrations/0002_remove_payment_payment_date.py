# Generated by Django 4.2.5 on 2023-09-19 16:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('booking_brain', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='payment',
            name='Payment_date',
        ),
    ]
