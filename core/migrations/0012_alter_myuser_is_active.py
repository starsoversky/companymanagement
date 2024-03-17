# Generated by Django 4.2.10 on 2024-03-07 20:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0011_alter_myuser_email"),
    ]

    operations = [
        migrations.AlterField(
            model_name="myuser",
            name="is_active",
            field=models.BooleanField(
                default=True,
                help_text="Designates whether this user should be treated as active. Unselect this instead of deleting accounts.",
                verbose_name="active",
            ),
        ),
    ]
