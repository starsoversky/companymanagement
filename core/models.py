from django.contrib.auth import get_user_model
from django.contrib.auth.models import (
    AbstractBaseUser,
    Group,
    Permission,
    PermissionsMixin,
    UserManager,
)
from django.core import validators
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

# User = get_user_model()


class MyUser(AbstractBaseUser, PermissionsMixin):
    USER_TYPE_CHOICES = (
        ("1", "Customer"),
        ("2", "Car Repair Company Agent"),
        ("3", "Insurance Agent"),
    )
    user_type = models.CharField(
        max_length=1, choices=USER_TYPE_CHOICES, null=True, blank=True
    )
    company = models.ForeignKey(
        "Company",
        on_delete=models.CASCADE,
        verbose_name=_("company"),
        related_name="company_user",
        blank=True,
        null=True,
    )
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
        _("email address"), max_length=255, unique=True, db_index=True
    )
    email_is_verified = models.BooleanField(default=False)
    fin_code = models.CharField(_("FIN"), max_length=100, unique=True)
    registration_number = models.CharField(
        max_length=255, unique=True, blank=True, null=True
    )
    address = models.CharField(max_length=100)
    phone_prefix = models.CharField(max_length=3)
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
    objects = UserManager()

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "User"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # cache current state of instance
        self.cache_is_active = self.is_active
        self.cache_is_staff = self.is_staff


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
        _("Registration date"), auto_now_add=True, db_index=True
    )

    def __str__(self):
        return "{name}".format(
            name=self.name,
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
    contract_number = models.CharField(max_length=100)
    customer_fin = models.CharField(_("Customer FIN"), max_length=100)
    coverage_plan = models.CharField(max_length=100)
    coverage_type = models.CharField(max_length=100)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

    def __str__(self):
        return "{customerfin}-{company}".format(
            customerfin=self.customer_fin, company=self.insurance_company
        )

    class Meta:
        verbose_name = "Insurance Policy"
        verbose_name_plural = "Insurance Policy"


class AgreementDocument(models.Model):
    insurance_company = models.ForeignKey(
        InsuranceCompany, related_name="agin_company", on_delete=models.CASCADE
    )
    insurance_agent = models.ForeignKey(
        InsuranceAgent, related_name="agin_agent", on_delete=models.CASCADE
    )
    car_repair_company = models.ForeignKey(
        CarRepairCompany, related_name="car_rep_company", on_delete=models.CASCADE
    )
    # car_repair_agent = models.ForeignKey(
    #     CarRepairCompanyAgent, related_name="car_rep_agent", on_delete=models.CASCADE
    # )
    services_to_provide = models.ManyToManyField(OfferedServices)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

    def __str__(self):
        return "{insurance_agent}-{car_repair_company}".format(
            insurance_agent=self.insurance_agent,
            car_repair_company=self.car_repair_company,
        )

    class Meta:
        verbose_name = "Insurance & Car Companies Agreement Document "
        verbose_name_plural = "Insurance & Car Companies Agreement Document "


class Vehicle(models.Model):
    customer = models.ForeignKey(
        CustomerUser,
        on_delete=models.CASCADE,
        related_name="cust_vehicle",
        blank=True,
        null=True,
    )
    insurance_policy = models.OneToOneField(
        InsurancePolicy,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="serv_doc",
    )
    customer_fin = models.CharField(
        _("Customer FIN"), max_length=100, blank=True, null=True
    )
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
        return "{customer_fin}".format(
            customer_fin=self.customer_fin,
        )

    class Meta:
        verbose_name = "Vehicle"
        verbose_name_plural = "Vehicle"


class Accident(models.Model):
    customer = models.ForeignKey(
        CustomerUser, on_delete=models.SET_NULL, related_name="accident_cust", null=True
    )
    # asset = models.ForeignKey(
    #     Asset, related_name="asset_case", on_delete=models.CASCADE
    # )
    insurance_policy = models.ForeignKey(
        InsurancePolicy,
        on_delete=models.CASCADE,
        related_name="accident_doc",
    )
    accident_date = models.DateField()
    accident_time = models.TimeField()
    location = models.CharField(max_length=255)
    description = models.TextField()
    # photos = models.ImageField(upload_to="uploads/")

    def __str__(self):
        return "{customer}||{insurance_policy}".format(
            customer=self.customer, insurance_policy=self.insurance_policy
        )

    class Meta:
        verbose_name = "Accident"
        verbose_name_plural = "Accident"

    def delete(self, *args, **kwargs):
        # Handle deletion of related objects first
        # self.acc_photos.all().delete()  # Assuming AccidentPhoto is related with ForeignKey
        # self.accident_bidding.delete()  # Assuming AccidentBidding is related with OneToOneField
        # self.appointment.delete()  # Assuming Appointment is related with OneToOneField
        # self.services_to_provide.all().clear()

        # Call the superclass method to delete the instance
        super().delete(*args, **kwargs)


class AccidentPhoto(models.Model):
    accident = models.ForeignKey(
        Accident, related_name="acc_photos", on_delete=models.CASCADE
    )
    photos = models.ImageField(upload_to="uploads/accident")


class AccidentBidding(models.Model):
    accident = models.OneToOneField(
        Accident, on_delete=models.CASCADE, related_name="accident_bidding"
    )
    insurance_company = models.ForeignKey(
        InsuranceCompany,
        on_delete=models.CASCADE,
        related_name="acc_comp",
    )
    insurance_company_agent = models.ForeignKey(
        InsuranceAgent, on_delete=models.SET_NULL, related_name="acc_compag", null=True
    )
    services_to_provide = models.ManyToManyField(OfferedServices)
    start_date = models.DateField(_("Accident bidding start date"))

    def __str__(self):
        return "{accident}".format(
            accident=self.accident,
        )

    class Meta:
        verbose_name = "Accident Bidding"
        verbose_name_plural = "Accident Bidding"

    def accepted_offers(self):
        return self.repair_offer.filter(accepted_offer=True).first()

    def delete(self, *args, **kwargs):
        # Handle deletion of related objects first
        self.repair_offer.all().delete()
        # self.acc_photos.all().delete()  # Assuming AccidentPhoto is related with ForeignKey
        # self.accident_bidding.delete()  # Assuming AccidentBidding is related with OneToOneField
        # self.appointment.delete()  # Assuming Appointment is related with OneToOneField
        # self.services_to_provide.all().clear()

        # Call the superclass method to delete the instance
        super().delete(*args, **kwargs)


class AccidentBiddingPhoto(models.Model):
    accident = models.ForeignKey(
        AccidentBidding, related_name="bidd_photos", on_delete=models.CASCADE
    )
    photos = models.ImageField(upload_to="uploads/bidding")


class CarRepairCompanyOffer(models.Model):
    offer_owner = models.ForeignKey(CarRepairCompany, on_delete=models.CASCADE)
    offer_owner_agent = models.ForeignKey(
        CarRepairCompanyAgent, on_delete=models.SET_NULL, null=True
    )
    accident_bidding = models.ForeignKey(
        AccidentBidding, on_delete=models.CASCADE, related_name="repair_offer"
    )
    services_to_provide = models.ManyToManyField(OfferedServices)
    repair_start_date = models.DateTimeField()
    approximate_budget = models.PositiveIntegerField()
    approximate_duration = models.DurationField()
    accepted_offer = models.BooleanField(default=False)
    rejected_offer = models.BooleanField(default=False)

    def __str__(self):
        return "{offer_owner}".format(
            offer_owner=self.offer_owner,
        )

    # @classmethod
    # def from_db(cls, db, field_names, values):
    #     instance = super().from_db(db, field_names, values)
    #     instance._cache_accepted_offer = instance.accepted_offer
    #     instance._cache_rejected_offer = instance.rejected_offer
    #     return instance

    class Meta:
        verbose_name = "Car Repair Company Offer"
        verbose_name_plural = "Car Repair Company Offer"

    def clean(self):
        if self.accepted_offer and self.rejected_offer:
            raise ValidationError(
                {
                    "rejected_offer": "Accepted offer and Rejected offer fields cannot be True at the same time."
                }
            )

    def delete(self, *args, **kwargs):
        # Handle deletion of related objects first
        # self.acc_photos.all().delete()  # Assuming AccidentPhoto is related with ForeignKey
        # self.accident_bidding.delete()  # Assuming AccidentBidding is related with OneToOneField
        # self.appointment.delete()  # Assuming Appointment is related with OneToOneField
        # self.services_to_provide.all().clear()

        # Call the superclass method to delete the instance
        super().delete(*args, **kwargs)


class Appointment(models.Model):
    STATUS = (
        ("1", "in progress"),
        ("2", "finished"),
        ("3", "scheduled"),
    )
    accident_bidding = models.OneToOneField(
        AccidentBidding,
        on_delete=models.CASCADE,
        related_name="appointment",
    )
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    customer = models.ForeignKey(CustomerUser, on_delete=models.CASCADE)
    status = models.CharField(max_length=1, choices=STATUS)
    date = models.DateTimeField()

    class Meta:
        verbose_name = "Appointment"
        verbose_name_plural = "Appointment"
