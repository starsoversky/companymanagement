# Generated by Django 3.0 on 2024-03-22 00:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20240322_0009'),
    ]

    operations = [
        migrations.AddField(
            model_name='myuser',
            name='phone_prefix',
            field=models.CharField(choices=[('1', '050'), ('2', '051'), ('3', '077'), ('3', '070'), ('3', '055'), ('3', '010'), ('3', '099'), ('3', '060')], default=1, max_length=3),
            preserve_default=False,
        ),
    ]