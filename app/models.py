from django.contrib.auth.models import AbstractBaseUser
from django.core import validators
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class UserCustomer(AbstractBaseUser):
    username = models.CharField(
        _("username"),
        max_length=50,
        unique=True,
        help_text=_(
            "Tələb olunur. 50 simvol və ya az. Hərflər, Rəqəmlər və "
            "@/./+/-/_ simvollar."
        ),
        validators=[
            validators.RegexValidator(
                r"^[\w.@+-]+$", _("Düzgün istifadəçi adı daxil edin."), "yanlışdır"
            )
        ],
    )
    first_name = models.CharField(_("first name"), max_length=100)
    last_name = models.CharField(_("last name"), max_length=100)
    email = models.EmailField(
        _("email address"), max_length=100, unique=True, db_index=True
    )
    fin_code = models.CharField(
        _("FIN Kod"),
        db_index=True,
        blank=True,
        null=True,
        max_length=100,
    )
    phone_number = models.CharField(max_length=20)
    address = models.CharField(max_length=100)
    registration_date = models.DateTimeField(
        _("date registration"), default=timezone.now
    )


class UserCompany(AbstractBaseUser):
    USER_TYPE_CHOICES = (
        ("A", "Company A"),
        ("B", "Company B"),
    )
    user_type = models.CharField(max_length=1, choices=USER_TYPE_CHOICES)
    username = models.CharField(
        _("username"),
        max_length=50,
        unique=True,
        help_text=_(
            "Tələb olunur. 50 simvol və ya az. Hərflər, Rəqəmlər və "
            "@/./+/-/_ simvollar."
        ),
        validators=[
            validators.RegexValidator(
                r"^[\w.@+-]+$", _("Düzgün istifadəçi adı daxil edin."), "yanlışdır"
            )
        ],
    )
    first_name = models.CharField(_("first name"), max_length=100)
    last_name = models.CharField(_("last name"), max_length=100)
    email = models.EmailField(
        _("email address"), max_length=100, unique=True, db_index=True
    )
    phone_number = models.CharField(max_length=20)
    address = models.CharField(max_length=100)
    registration_number = models.CharField(max_length=255, unique=True)
    registration_date = models.DateTimeField(
        _("date registration"), default=timezone.now
    )


class CompanyA(models.Model):

    user = models.OneToOneField(
        UserCompany, on_delete=models.CASCADE, related_name="company_a"
    )
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20)
    address = models.CharField(max_length=255)
    email = models.EmailField()
    registration_number = models.CharField(max_length=255, unique=True)
    registration_date = models.DateTimeField(
        _("date registration"), default=timezone.now
    )


class CompanyB(models.Model):
    user = models.OneToOneField(
        UserCompany, on_delete=models.CASCADE, related_name="company_b"
    )
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20)
    address = models.CharField(max_length=255)
    email = models.EmailField()
    registration_date = models.DateTimeField(
        _("date registration"), default=timezone.now
    )


class CompanyDocument(models.Model):
    customer = models.ForeignKey(
        UserCustomer, related_name="comp_doc", on_delete=models.CASCADE
    )
    company_a = models.ForeignKey(
        CompanyA, related_name="comp_doc", on_delete=models.CASCADE
    )
    company_user = models.ForeignKey(
        UserCompany, related_name="company_user", on_delete=models.CASCADE
    )
    service_plan = models.CharField(max_length=100)
    service_type = models.CharField(max_length=100)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()


class Asset(models.Model):
    customer = models.ForeignKey(
        UserCustomer, on_delete=models.CASCADE, related_name="cust_asset"
    )
    service_document = models.ForeignKey(
        CompanyDocument, on_delete=models.CASCADE, related_name="serv_doc"
    )
    brand = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    year = models.IntegerField()
    color = models.CharField(max_length=100)
    category = models.CharField(max_length=255)
    capacity = models.IntegerField(default=0)
    power = models.CharField(max_length=100)
    structure = models.CharField(max_length=100)
    vin_code = models.CharField(max_length=100)
    plate_number = models.CharField(max_length=100)


class Case(models.Model):
    customer = models.ForeignKey(
        UserCustomer, on_delete=models.CASCADE, related_name="reported_cases"
    )
    company_user = models.ForeignKey(
        UserCompany, related_name="case_user", on_delete=models.CASCADE
    )
    document = models.ForeignKey(
        CompanyDocument, related_name="case_document", on_delete=models.CASCADE
    )

    date = models.DateField()
    time = models.TimeField()
    location = models.CharField(max_length=255)
    description = models.TextField()
    photos = models.ImageField(upload_to="uploads/")
    competition_start_date = models.DateField()


class Competition(models.Model):
    case = models.ForeignKey(
        Case, on_delete=models.CASCADE, related_name="competitions"
    )
    company_b = models.ForeignKey(
        UserCompany, on_delete=models.CASCADE, related_name="competition"
    )
    submission_date = models.DateTimeField(auto_now_add=True)
    start_date = models.DateTimeField()
    estimated_cost = models.DecimalField(max_digits=10, decimal_places=2)
    restoration_duration = models.DurationField()
    close_date = models.DateTimeField()
    winner = models.BooleanField()


class Meeting(models.Model):
    STATUS = (
        ("A", "in progress"),
        ("B", "finished"),
        ("C", "scheduled"),
    )
    competation = models.OneToOneField(
        Case, on_delete=models.CASCADE, related_name="meeting"
    )
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE)
    customer = models.ForeignKey(UserCustomer, on_delete=models.CASCADE)
    status = models.CharField(max_length=1, choices=STATUS)
    date = models.DateTimeField()
    time = models.TimeField()

    # Other company profile details
