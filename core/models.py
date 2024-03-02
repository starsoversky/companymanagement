from django.contrib.auth import get_user_model
from django.contrib.auth.models import (
    AbstractBaseUser,
    AbstractUser,
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
        ("A", "Company A"),
        ("B", "Company B"),
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
    fin_code = models.CharField(max_length=100, blank=True, null=True)
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
        verbose_name = "İstifadəçilər"
        verbose_name_plural = "İstifadəçilər"

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


class CompanyAUser(MyUser):

    class Meta:
        proxy = True

    def __str__(self):
        return "{username}".format(
            username=self.username,
        )


class CompanyBUser(MyUser):

    class Meta:
        proxy = True

    def __str__(self):
        return "{username}".format(
            username=self.username,
        )


# class Customer(AbstractUser, PermissionsMixin):
#     username = models.CharField(
#         _("username"),
#         max_length=50,
#         unique=True,
#         help_text=_(
#             "Tələb olunur. 50 simvol və ya az. Hərflər, Rəqəmlər və "
#             "@/./+/-/_ simvollar."
#         ),
#         validators=[
#             validators.RegexValidator(
#                 r"^[\w.@+-]+$", _("Düzgün istifadəçi adı daxil edin."), "yanlışdır"
#             )
#         ],
#     )
#     first_name = models.CharField(_("first name"), max_length=100)
#     last_name = models.CharField(_("last name"), max_length=100)
#     email = models.EmailField(
#         _("email address"), max_length=100, unique=True, db_index=True
#     )
#     fin_code = models.CharField(
#         _("FIN Kod"),
#         db_index=True,
#         blank=True,
#         null=True,
#         max_length=100,
#     )
#     phone_number = models.CharField(max_length=20)
#     address = models.CharField(max_length=100)
#     registration_date = models.DateTimeField(
#         _("date registration"), default=timezone.now
#     )
#     groups = models.ManyToManyField(
#         Group,
#         verbose_name=_("groups"),
#         blank=True,
#         help_text=_(
#             "The groups this user belongs to. A user will get all permissions "
#             "granted to each of their groups."
#         ),
#         related_name="customer_user_set",
#         related_query_name="customer_user",
#     )
#     user_permissions = models.ManyToManyField(
#         Permission,
#         verbose_name=_("user permissions"),
#         blank=True,
#         help_text=_("Specific permissions for this user."),
#         related_name="myuser_set",
#         related_query_name="myuser",
#     )
#     USERNAME_FIELD = "username"
#     EMAIL_FIELD = "email"

#     class Meta:
#         verbose_name = "Musteriler"
#         verbose_name_plural = "Musteriler"


class Company(models.Model):
    COMPANY_TYPE_CHOICES = (
        ("A", "Company A"),
        ("B", "Company B"),
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
    registration_number = models.CharField(max_length=255, unique=True)
    registration_date = models.DateTimeField(
        _("date registration"), default=timezone.now
    )


class CompanyA(Company):

    class Meta:
        proxy = True

    def __str__(self):
        return "{name}".format(
            name=self.name,
        )


class CompanyB(Company):
    class Meta:
        proxy = True

    def __str__(self):
        return "{name}".format(
            name=self.name,
        )


class CompanyDocument(models.Model):
    customer = models.ForeignKey(
        CustomerUser,
        related_name="comp_doc",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    company_a = models.ForeignKey(
        CompanyA, related_name="comp_doc", on_delete=models.CASCADE
    )
    company_user = models.ForeignKey(
        CompanyAUser, related_name="company_user", on_delete=models.CASCADE
    )
    customer_fin = models.CharField(max_length=100)
    service_plan = models.CharField(max_length=100)
    service_type = models.CharField(max_length=100)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()


class AgreementDocument(models.Model):
    owner = models.ForeignKey(
        CompanyB, related_name="ag_owner", on_delete=models.CASCADE
    )
    company_a = models.ForeignKey(
        CompanyA, related_name="ag_doc", on_delete=models.CASCADE
    )
    services_to_provide = models.CharField(max_length=100)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()


class Asset(models.Model):
    customer = models.ForeignKey(
        CustomerUser,
        on_delete=models.CASCADE,
        related_name="cust_asset",
        blank=True,
        null=True,
    )
    service_document = models.OneToOneField(
        CompanyDocument,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="serv_doc",
    )
    customer_fin = models.CharField(max_length=100)
    brand = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    year = models.IntegerField()
    color = models.CharField(max_length=100)
    category = models.CharField(max_length=255)
    capacity = models.IntegerField(default=0)
    power = models.CharField(max_length=100)
    structure = models.CharField(max_length=100)
    vin_code = models.CharField(max_length=100, unique=True)
    plate_number = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return "{brand}".format(
            brand=self.brand,
        )

    class Meta:
        verbose_name = "Cihaz"
        verbose_name_plural = "Cihaz"


class Case(models.Model):
    customer = models.ForeignKey(
        CustomerUser, on_delete=models.CASCADE, related_name="case_cust"
    )
    # asset = models.ForeignKey(
    #     Asset, related_name="asset_case", on_delete=models.CASCADE
    # )
    service_document = models.OneToOneField(
        CompanyDocument,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="case_doc",
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
    company = models.ForeignKey(
        CompanyA, on_delete=models.CASCADE, related_name="comp_company"
    )
    submission_date = models.DateTimeField(auto_now_add=True)
    start_date = models.DateTimeField()
    estimated_cost = models.DecimalField(max_digits=10, decimal_places=2)
    restoration_duration = models.DurationField()
    close_date = models.DateTimeField()
    # winner = models.BooleanField()


class CompanyOffer(models.Model):
    offer_owner = models.ForeignKey(CompanyB, on_delete=models.CASCADE)
    competition = models.ForeignKey(Competition, on_delete=models.CASCADE)
    services_offered = models.CharField(max_length=255)
    winner = models.BooleanField()
    reject = models.BooleanField()


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
    customer = models.ForeignKey(CustomerUser, on_delete=models.CASCADE)
    status = models.CharField(max_length=1, choices=STATUS)
    date = models.DateTimeField()
    time = models.TimeField()

    # Other company profile details
