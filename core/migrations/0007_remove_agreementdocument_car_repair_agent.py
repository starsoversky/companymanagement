# Generated by Django 3.0.3 on 2024-03-23 21:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_auto_20240323_1556'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='agreementdocument',
            name='car_repair_agent',
        ),
    ]
