from django.contrib.auth import get_user_model
from django.contrib.auth.models import (
    AbstractBaseUser,
    Group,
    Permission,
    PermissionsMixin,
    UserManager,
)
from django.core import validators
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

# User = get_user_model()


class MyUser(AbstractBaseUser, PermissionsMixin):
    USER_TYPE_CHOICES = (
        ("A", "Insurance Agent"),
        ("B", "Car Repair Company Agent"),
        ("C", "Customer"),
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
    fin_code = models.CharField(_("FIN"), max_length=100, blank=True, null=True)
    registration_number = models.CharField(
        max_length=255, unique=True, blank=True, null=True
    )
    address = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20)
    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_("Designates whether the user can log into this admin " "site."),
    )
    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as "
            "active. Unselect this instead of deleting accounts."
        ),
    )
    is_blocked = models.BooleanField(
        default=False,
        help_text=_(
            "Designates whether this user should be treated as "
            "block. Unselect this instead of deleting accounts."
        ),
    )

    is_admin = models.BooleanField(
        _("əsas istifadəçi statusu"),
        default=False,
        help_text=_("Designates whether the user is base user on web site."),
    )

    date_joined = models.DateTimeField(_("date joined"), default=timezone.now)
    groups = models.ManyToManyField(
        Group,
        verbose_name=_("groups"),
        blank=True,
        help_text=_(
            "The groups this user belongs to. A user will get all permissions "
            "granted to each of their groups."
        ),
        related_name="company_user_set",
        related_query_name="myuser",
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name=_("user permissions"),
        blank=True,
        help_text=_("Specific permissions for this user."),
        related_name="company_user_set",
        related_query_name="myuser",
    )
    objects = UserManager()

    USERNAME_FIELD = "username"
    EMAIL_FIELD = "email"

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "User"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # cache current state of instance
        self.cache_is_active = self.is_active


class CustomerUser(MyUser):

    class Meta:
        proxy = True

    def __str__(self):
        return "{username}".format(
            username=self.username,
        )


class InsuranceAgent(MyUser):

    class Meta:
        proxy = True

    def __str__(self):
        return "{username}".format(
            username=self.username,
        )


class CarRepairCompanyAgent(MyUser):

    class Meta:
        proxy = True

    def __str__(self):
        return "{username}".format(
            username=self.username,
        )


class Company(models.Model):
    COMPANY_TYPE_CHOICES = (
        ("A", "Insurance Company"),
        ("B", "Car Repair Company"),
    )
    type = models.CharField(max_length=1, choices=COMPANY_TYPE_CHOICES)

    # user = models.OneToOneField(
    #     CompanyAUser,
    #     on_delete=models.CASCADE,
    #     related_name="%(app_label)s_%(class)s_related",
    # )
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20)
    address = models.CharField(max_length=255)
    email = models.EmailField()
    # services_offered=
    registration_number = models.CharField(max_length=255, unique=True)
    registration_date = models.DateTimeField(
        _("date registration"), default=timezone.now
    )

    class Meta:
        verbose_name = "Company"
        verbose_name_plural = "Company"


class OfferedServices(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return "{name}".format(
            name=self.name,
        )

    class Meta:
        verbose_name = "Offered Services"
        verbose_name_plural = "Offered Services"


class InsuranceCompany(Company):

    class Meta:
        proxy = True

    def __str__(self):
        return "{name}".format(
            name=self.name,
        )

    class Meta:
        verbose_name = "Insurance Company"
        verbose_name_plural = "Insurance Company"


class CarRepairCompany(Company):
    class Meta:
        proxy = True

    def __str__(self):
        return "{name}".format(
            name=self.name,
        )

    class Meta:
        verbose_name = "Car Repair Company"
        verbose_name_plural = "Car Repair Company"


class InsurancePolicy(models.Model):
    customer = models.ForeignKey(
        CustomerUser,
        related_name="comp_doc",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    insurance_company = models.ForeignKey(
        InsuranceCompany, related_name="insurance_company", on_delete=models.CASCADE
    )
    insurance_agent = models.ForeignKey(
        InsuranceAgent, related_name="insurance_agent", on_delete=models.CASCADE
    )
    customer_fin = models.CharField(_("Customer FIN"), max_length=100)
    coverage_plan = models.CharField(max_length=100)
    coverage_type = models.CharField(max_length=100)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

    class Meta:
        verbose_name = "Insurance Policy"
        verbose_name_plural = "Insurance Policy"


class AgreementDocument(models.Model):
    insurance_agent = models.ForeignKey(
        InsuranceCompany, related_name="insurance_agent", on_delete=models.CASCADE
    )
    car_repair_company = models.ForeignKey(
        CarRepairCompany, related_name="car_repair_company", on_delete=models.CASCADE
    )
    services_to_provide = models.ManyToManyField(OfferedServices)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

    class Meta:
        verbose_name = "Agreement Document"
        verbose_name_plural = "Agreement Document"


class Vehicle(models.Model):
    customer = models.ForeignKey(
        CustomerUser,
        on_delete=models.CASCADE,
        related_name="cust_vehicle",
        blank=True,
        null=True,
    )
    service_document = models.OneToOneField(
        InsurancePolicy,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="serv_doc",
    )
    customer_fin = models.CharField(_("Customer FIN"), max_length=100)
    make = models.CharField(max_length=255)
    model = models.CharField(max_length=100)
    year = models.IntegerField()
    color = models.CharField(max_length=100)
    type = models.CharField(max_length=255)
    seating_capacity = models.IntegerField(default=0)
    engine = models.CharField(max_length=100)
    body = models.CharField(max_length=100)
    plate_number = models.CharField(max_length=100, unique=True)
    vin = models.CharField(_("VIN"), max_length=100, unique=True)

    def __str__(self):
        return "{brand}".format(
            brand=self.brand,
        )

    class Meta:
        verbose_name = "Vehicle"
        verbose_name_plural = "Vehicle"


class Accident(models.Model):
    customer = models.ForeignKey(
        CustomerUser, on_delete=models.CASCADE, related_name="accident_cust"
    )
    # asset = models.ForeignKey(
    #     Asset, related_name="asset_case", on_delete=models.CASCADE
    # )
    service_document = models.OneToOneField(
        InsurancePolicy,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="accident_doc",
    )
    date = models.DateField()
    accident_time = models.TimeField()
    location = models.CharField(max_length=255)
    description = models.TextField()
    photos = models.ImageField(upload_to="uploads/")
    accidentbidding_start_date = models.DateField(_("Accident bidding start date"))

    class Meta:
        verbose_name = "Accident"
        verbose_name_plural = "Accident"


class AccidentBidding(models.Model):
    accident = models.ForeignKey(
        Accident, on_delete=models.CASCADE, related_name="accident_bidding"
    )
    company = models.ForeignKey(
        InsuranceCompany, on_delete=models.CASCADE, related_name="comp_company"
    )
    # submission_date = models.DateTimeField(auto_now_add=True)
    # repair_start_date = models.DateTimeField()
    # estimated_cost = models.DecimalField(max_digits=10, decimal_places=2)
    # restoration_duration = models.DurationField()
    # close_date = models.DateTimeField()
    # winner = models.BooleanField()

    class Meta:
        verbose_name = "Accident Bidding"
        verbose_name_plural = "Accident Bidding"


class CarInsuranceDocument(models.Model):
    offer_owner = models.ForeignKey(CarRepairCompany, on_delete=models.CASCADE)
    accident_bidding = models.ForeignKey(AccidentBidding, on_delete=models.CASCADE)
    services_to_provide = models.ManyToManyField(OfferedServices)
    winner = models.BooleanField()
    reject = models.BooleanField()

    class Meta:
        verbose_name = "Car Insurance Document"
        verbose_name_plural = "Car Insurance Document"


class Appointment(models.Model):
    STATUS = (
        ("A", "in progress"),
        ("B", "finished"),
        ("C", "scheduled"),
    )
    accidentbidding = models.OneToOneField(
        AccidentBidding, on_delete=models.CASCADE, related_name="appointment"
    )
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    customer = models.ForeignKey(CustomerUser, on_delete=models.CASCADE)
    status = models.CharField(max_length=1, choices=STATUS)
    date = models.DateTimeField()
    time = models.TimeField()

    class Meta:
        verbose_name = "Appointment"
        verbose_name_plural = "Appointment"
