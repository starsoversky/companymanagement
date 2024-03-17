# Generated by Django 4.2.10 on 2024-03-11 23:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0014_alter_company_registration_date"),
    ]

    operations = [
        migrations.AddField(
            model_name="myuser",
            name="company",
            field=models.ForeignKey(
                default=3,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="company_user",
                to="core.company",
                verbose_name="company",
            ),
            preserve_default=False,
        ),
    ]
