# Generated by Django 3.0.3 on 2024-04-06 21:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0017_myuser_email_is_verified'),
    ]

    operations = [
        migrations.AlterField(
            model_name='accident',
            name='insurance_policy',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='accident_doc', to='core.InsurancePolicy'),
        ),
        migrations.AlterField(
            model_name='myuser',
            name='phone_prefix',
            field=models.CharField(max_length=3),
        ),
    ]
