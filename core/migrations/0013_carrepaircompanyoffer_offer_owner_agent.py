# Generated by Django 4.2.10 on 2024-03-09 19:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0012_alter_myuser_is_active"),
    ]

    operations = [
        migrations.AddField(
            model_name="carrepaircompanyoffer",
            name="offer_owner_agent",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                to="core.carrepaircompanyagent",
            ),
            preserve_default=False,
        ),
    ]
