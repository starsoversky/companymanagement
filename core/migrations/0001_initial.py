# Generated by Django 4.2.10 on 2024-03-03 14:57

import django.contrib.auth.models
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("auth", "0012_alter_user_first_name_max_length"),
    ]

    operations = [
        migrations.CreateModel(
            name="Accident",
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
                ("accident_date", models.DateField()),
                ("accident_time", models.TimeField()),
                ("location", models.CharField(max_length=255)),
                ("description", models.TextField()),
                ("photos", models.ImageField(upload_to="uploads/")),
            ],
            options={
                "verbose_name": "Accident",
                "verbose_name_plural": "Accident",
            },
        ),
        migrations.CreateModel(
            name="AccidentBidding",
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
                (
                    "start_date",
                    models.DateField(verbose_name="Accident bidding start date"),
                ),
                (
                    "accident",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="accident_bidding",
                        to="core.accident",
                    ),
                ),
            ],
            options={
                "verbose_name": "Accident Bidding",
                "verbose_name_plural": "Accident Bidding",
            },
        ),
        migrations.CreateModel(
            name="Company",
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
                (
                    "type",
                    models.CharField(
                        choices=[
                            ("A", "Insurance Company"),
                            ("B", "Car Repair Company"),
                        ],
                        max_length=1,
                    ),
                ),
                ("name", models.CharField(max_length=100)),
                ("phone_number", models.CharField(max_length=20)),
                ("address", models.CharField(max_length=255)),
                ("email", models.EmailField(max_length=254)),
                ("registration_number", models.CharField(max_length=255, unique=True)),
                (
                    "registration_date",
                    models.DateTimeField(
                        default=django.utils.timezone.now,
                        verbose_name="Registration date",
                    ),
                ),
            ],
            options={
                "verbose_name": "Company",
                "verbose_name_plural": "Company",
            },
        ),
        migrations.CreateModel(
            name="InsurancePolicy",
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
                (
                    "customer_fin",
                    models.CharField(max_length=100, verbose_name="Customer FIN"),
                ),
                ("coverage_plan", models.CharField(max_length=100)),
                ("coverage_type", models.CharField(max_length=100)),
                ("start_date", models.DateTimeField()),
                ("end_date", models.DateTimeField()),
            ],
            options={
                "verbose_name": "Insurance Policy",
                "verbose_name_plural": "Insurance Policy",
            },
        ),
        migrations.CreateModel(
            name="OfferedServices",
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
                ("name", models.CharField(max_length=255)),
            ],
            options={
                "verbose_name": "Offered Services",
                "verbose_name_plural": "Offered Services",
            },
        ),
        migrations.CreateModel(
            name="CarRepairCompany",
            fields=[
                (
                    "company_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="core.company",
                    ),
                ),
            ],
            options={
                "verbose_name": "Car Repair Company",
                "verbose_name_plural": "Car Repair Company",
            },
            bases=("core.company",),
        ),
        migrations.CreateModel(
            name="InsuranceCompany",
            fields=[
                (
                    "company_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="core.company",
                    ),
                ),
            ],
            options={
                "verbose_name": "Insurance Company",
                "verbose_name_plural": "Insurance Company",
            },
            bases=("core.company",),
        ),
        migrations.AddField(
            model_name="accident",
            name="insurance_policy",
            field=models.OneToOneField(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="accident_doc",
                to="core.insurancepolicy",
            ),
        ),
        migrations.CreateModel(
            name="MyUser",
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
                ("password", models.CharField(max_length=128, verbose_name="password")),
                (
                    "last_login",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="last login"
                    ),
                ),
                (
                    "is_superuser",
                    models.BooleanField(
                        default=False,
                        help_text="Designates that this user has all permissions without explicitly assigning them.",
                        verbose_name="superuser status",
                    ),
                ),
                (
                    "user_type",
                    models.CharField(
                        choices=[
                            ("A", "Insurance Agent"),
                            ("B", "Car Repair Company Agent"),
                            ("C", "Customer"),
                        ],
                        max_length=1,
                    ),
                ),
                (
                    "username",
                    models.CharField(
                        help_text="Tələb olunur. 50 simvol və ya az. Hərflər, Rəqəmlər və @/./+/-/_ simvollar.",
                        max_length=50,
                        unique=True,
                        validators=[
                            django.core.validators.RegexValidator(
                                "^[\\w.@+-]+$",
                                "Düzgün istifadəçi adı daxil edin.",
                                "yanlışdır",
                            )
                        ],
                        verbose_name="username",
                    ),
                ),
                (
                    "first_name",
                    models.CharField(max_length=100, verbose_name="first name"),
                ),
                (
                    "last_name",
                    models.CharField(max_length=100, verbose_name="last name"),
                ),
                (
                    "email",
                    models.EmailField(
                        db_index=True,
                        max_length=100,
                        unique=True,
                        verbose_name="email address",
                    ),
                ),
                (
                    "fin_code",
                    models.CharField(
                        blank=True, max_length=100, null=True, verbose_name="FIN"
                    ),
                ),
                (
                    "registration_number",
                    models.CharField(
                        blank=True, max_length=255, null=True, unique=True
                    ),
                ),
                ("address", models.CharField(max_length=100)),
                ("phone_number", models.CharField(max_length=20)),
                (
                    "is_staff",
                    models.BooleanField(
                        default=False,
                        help_text="Designates whether the user can log into this admin site.",
                        verbose_name="staff status",
                    ),
                ),
                (
                    "is_active",
                    models.BooleanField(
                        default=True,
                        help_text="Designates whether this user should be treated as active. Unselect this instead of deleting accounts.",
                        verbose_name="active",
                    ),
                ),
                (
                    "is_blocked",
                    models.BooleanField(
                        default=False,
                        help_text="Designates whether this user should be treated as block. Unselect this instead of deleting accounts.",
                    ),
                ),
                (
                    "is_admin",
                    models.BooleanField(
                        default=False,
                        help_text="Designates whether the user is base user on web site.",
                        verbose_name="əsas istifadəçi statusu",
                    ),
                ),
                (
                    "date_joined",
                    models.DateTimeField(
                        default=django.utils.timezone.now, verbose_name="date joined"
                    ),
                ),
                (
                    "groups",
                    models.ManyToManyField(
                        blank=True,
                        help_text="The groups this user belongs to. A user will get all permissions granted to each of their groups.",
                        related_name="company_user_set",
                        related_query_name="myuser",
                        to="auth.group",
                        verbose_name="groups",
                    ),
                ),
                (
                    "user_permissions",
                    models.ManyToManyField(
                        blank=True,
                        help_text="Specific permissions for this user.",
                        related_name="company_user_set",
                        related_query_name="myuser",
                        to="auth.permission",
                        verbose_name="user permissions",
                    ),
                ),
            ],
            options={
                "verbose_name": "User",
                "verbose_name_plural": "User",
            },
            managers=[
                ("objects", django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name="CarRepairCompanyAgent",
            fields=[],
            options={
                "proxy": True,
                "indexes": [],
                "constraints": [],
            },
            bases=("core.myuser",),
            managers=[
                ("objects", django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name="CustomerUser",
            fields=[],
            options={
                "proxy": True,
                "indexes": [],
                "constraints": [],
            },
            bases=("core.myuser",),
            managers=[
                ("objects", django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name="InsuranceAgent",
            fields=[],
            options={
                "proxy": True,
                "indexes": [],
                "constraints": [],
            },
            bases=("core.myuser",),
            managers=[
                ("objects", django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name="Vehicle",
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
                (
                    "customer_fin",
                    models.CharField(max_length=100, verbose_name="Customer FIN"),
                ),
                ("make", models.CharField(max_length=255)),
                ("model", models.CharField(max_length=100)),
                ("year", models.IntegerField()),
                ("color", models.CharField(max_length=100)),
                ("type", models.CharField(max_length=255)),
                ("seating_capacity", models.IntegerField(default=0)),
                ("engine", models.CharField(max_length=100)),
                ("body", models.CharField(max_length=100)),
                ("plate_number", models.CharField(max_length=100, unique=True)),
                (
                    "vin",
                    models.CharField(max_length=100, unique=True, verbose_name="VIN"),
                ),
                (
                    "insurance_policy",
                    models.OneToOneField(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="serv_doc",
                        to="core.insurancepolicy",
                    ),
                ),
                (
                    "customer",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="cust_vehicle",
                        to="core.customeruser",
                    ),
                ),
            ],
            options={
                "verbose_name": "Vehicle",
                "verbose_name_plural": "Vehicle",
            },
        ),
        migrations.AddField(
            model_name="insurancepolicy",
            name="customer",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="comp_doc",
                to="core.customeruser",
            ),
        ),
        migrations.AddField(
            model_name="insurancepolicy",
            name="insurance_agent",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="insurance_agent",
                to="core.insuranceagent",
            ),
        ),
        migrations.AddField(
            model_name="insurancepolicy",
            name="insurance_company",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="insurance_company",
                to="core.insurancecompany",
            ),
        ),
        migrations.CreateModel(
            name="CarRepairCompanyOffer",
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
                ("repair_start_date", models.DateTimeField()),
                ("approximate_budget", models.PositiveBigIntegerField()),
                ("approximate_duration", models.DurationField()),
                ("accepted_offer", models.BooleanField()),
                ("rejected_offer", models.BooleanField()),
                (
                    "accident_bidding",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="repair_offer",
                        to="core.accidentbidding",
                    ),
                ),
                (
                    "services_to_provide",
                    models.ManyToManyField(to="core.offeredservices"),
                ),
                (
                    "offer_owner",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="core.carrepaircompany",
                    ),
                ),
            ],
            options={
                "verbose_name": "Car Repair Company Offer",
                "verbose_name_plural": "Car Repair Company Offer",
            },
        ),
        migrations.CreateModel(
            name="Appointment",
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
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("A", "in progress"),
                            ("B", "finished"),
                            ("C", "scheduled"),
                        ],
                        max_length=1,
                    ),
                ),
                ("date", models.DateTimeField()),
                (
                    "accident_bidding",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="appointment",
                        to="core.accidentbidding",
                    ),
                ),
                (
                    "vehicle",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="core.vehicle"
                    ),
                ),
                (
                    "customer",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="core.customeruser",
                    ),
                ),
            ],
            options={
                "verbose_name": "Appointment",
                "verbose_name_plural": "Appointment",
            },
        ),
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
                ("start_date", models.DateTimeField()),
                ("end_date", models.DateTimeField()),
                (
                    "services_to_provide",
                    models.ManyToManyField(to="core.offeredservices"),
                ),
                (
                    "car_repair_agent",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="car_rep_agent",
                        to="core.carrepaircompanyagent",
                    ),
                ),
                (
                    "car_repair_company",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="car_rep_company",
                        to="core.carrepaircompany",
                    ),
                ),
                (
                    "insurance_agent",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="agin_agent",
                        to="core.insuranceagent",
                    ),
                ),
                (
                    "insurance_company",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="agin_company",
                        to="core.insurancecompany",
                    ),
                ),
            ],
            options={
                "verbose_name": "Agreement Document",
                "verbose_name_plural": "Agreement Document",
            },
        ),
        migrations.AddField(
            model_name="accidentbidding",
            name="company",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="comp_company",
                to="core.insurancecompany",
            ),
        ),
        migrations.AddField(
            model_name="accident",
            name="customer",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="accident_cust",
                to="core.customeruser",
            ),
        ),
    ]
