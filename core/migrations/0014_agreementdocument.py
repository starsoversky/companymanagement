# Generated by Django 4.2.10 on 2024-03-02 17:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0013_alter_competition_company"),
    ]

    operations = [
        migrations.CreateModel(
            name="AgreementDocument",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("services_to_provide", models.CharField(max_length=100)),
                ("start_date", models.DateTimeField()),
                ("end_date", models.DateTimeField()),
                (
                    "company_a",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="ag_doc",
                        to="core.companya",
                    ),
                ),
                (
                    "owner",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="ag_owner",
                        to="core.companyb",
                    ),
                ),
            ],
        ),
    ]
