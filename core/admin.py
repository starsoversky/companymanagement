from typing import Any

from django.contrib import admin
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.core.exceptions import ValidationError
from django.db.models import Q
from django.utils.translation import gettext_lazy as _

from core.admin_filter import AccidentBiddingFilter

from .forms import MyUserChangeForm

# from .forms import CarInsuranceDocumentAdminForm
from .models import *

User = get_user_model()


@admin.register(User)
class MyUserAdmin(UserAdmin):
    # readonly_fields = ("company",)
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (
            _("Personal info"),
            {
                "fields": (
                    "user_type",
                    "first_name",
                    "last_name",
                    "email",
                    "fin_code",
                    "registration_number",
                    "address",
                    "phone_prefix",
                    "phone_number",
                    "company",
                )
            },
        ),
        (
            _("Permissions"),
            {
                "fields": (
                    "email_is_verified",
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "is_admin",
                    "is_blocked",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "first_name",
                    "last_name",
                    "username",
                    "password1",
                    "password2",
                    "email",
                    "fin_code",
                    "registration_number",
                    "address",
                    "phone_prefix",
                    "phone_number",
                ),
            },
        ),
    )
    form = MyUserChangeForm
    list_display = ("username", "is_staff", "user_type")
    list_filter = ("is_staff", "is_superuser", "is_active", "groups", "user_type")
    ordering = ("-date_joined",)
    filter_horizontal = (
        "groups",
        "user_permissions",
    )

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        if request.user.is_staff and not request.user.is_superuser:
            if request.user.user_type == "3":  # Assuming '3' represents Insurance Agent
                # Get the insurance policies associated with the Insurance Agent's company
                insurance_policies = InsurancePolicy.objects.filter(
                    insurance_company=request.user.company
                )
                # Get the Customer users associated with these insurance policies
                queryset = User.objects.filter(
                    Q(user_type="1", comp_doc__in=insurance_policies)
                    | Q(company=request.user.company)
                )

            return queryset.distinct()
        return queryset

    def save_model(self, request, obj, form, change):
        return super().save_model(request, obj, form, change)


@admin.register(InsuranceCompany)
class InsuranceCompanyAdmin(admin.ModelAdmin):
    pass


@admin.register(CarRepairCompany)
class CarRepairCompanyAdmin(admin.ModelAdmin):
    readonly_fields = ("registration_date",)


@admin.register(InsurancePolicy)
class InsurancePolicyAdmin(admin.ModelAdmin):
    readonly_fields = ("insurance_agent",)

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        if request.user.is_staff and not request.user.is_superuser:
            if request.user.user_type == "3":  # Assuming '3' represents Insurance Agent
                # Get the insurance policies associated with the Insurance Agent's company
                queryset = InsurancePolicy.objects.filter(
                    insurance_company=request.user.company
                )
        return queryset

    def save_model(self, request, obj, form, change):
        if obj:
            obj.insurance_agent = request.user
        super().save_model(request, obj, form, change)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if not request.user.is_superuser:
            if db_field.name == "customer":
                # Customize the queryset here
                kwargs["queryset"] = CustomerUser.objects.filter(
                    user_type=1, is_active=True
                )
            if db_field.name == "insurance_company":
                # Customize the queryset here
                if request.user.company:
                    kwargs["queryset"] = InsuranceCompany.objects.filter(
                        id=request.user.company.id
                    )
                else:
                    kwargs["queryset"] = InsuranceCompany.objects.none()
            # if db_field.name == "insurance_agent":
            #     # Customize the queryset here
            #     kwargs["queryset"] = InsuranceCompany.objects.filter(
            #         id=request.user.company.id
            #     )
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        if request.user.is_staff and not request.user.is_superuser:
            if request.user.user_type == "3":  # Assuming '3' represents Insurance Agent
                # Get the insurance policies associated with the Insurance Agent's company
                queryset = Vehicle.objects.filter(
                    insurance_policy__insurance_company=request.user.company
                )
        return queryset

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if not request.user.is_superuser:
            if db_field.name == "customer":
                # Customize the queryset here
                kwargs["queryset"] = CustomerUser.objects.filter(
                    user_type=1, is_active=True
                )
            if db_field.name == "insurance_policy":
                # Customize the queryset here
                kwargs["queryset"] = InsurancePolicy.objects.filter(
                    insurance_company=request.user.company
                )
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class AccidentPhotoInline(admin.TabularInline):
    model = AccidentPhoto


@admin.register(Accident)
class AccidentAdmin(admin.ModelAdmin):
    inlines = [AccidentPhotoInline]
    list_display = ("customer", "insurance_policy", "accident_date")

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        if not request.user.is_superuser:
            queryset = Accident.objects.filter(
                insurance_policy__insurance_company=request.user.company
            )
        return queryset


class AccidentBiddingPhotoInline(admin.TabularInline):
    model = AccidentBiddingPhoto


@admin.register(AccidentBidding)
class AccidentBiddingAdmin(admin.ModelAdmin):
    inlines = [AccidentBiddingPhotoInline]
    readonly_fields = [
        "accepted_offers",
        "insurance_company_agent",
        "insurance_company",
    ]

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        if request.user.is_staff and not request.user.is_superuser:
            if request.user.user_type == "3":  # Assuming '3' represents Insurance Agent
                queryset = queryset.filter(insurance_company=request.user.company)
            return queryset.distinct()
        return queryset

    def save_model(self, request, obj, form, change):
        if obj and not request.user.is_superuser:
            if request.user.user_type == "3":
                obj.insurance_company_agent = request.user
                if request.user.company:

                    obj.insurance_company_id = request.user.company.id
        super().save_model(request, obj, form, change)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if not request.user.is_superuser:
            if db_field.name == "accident":
                # Customize the queryset here
                kwargs["queryset"] = Accident.objects.filter(
                    insurance_policy__insurance_company=request.user.company
                )
            # if db_field.name == "insurance_company":
            #     # Customize the queryset here
            #     kwargs["queryset"] = InsuranceCompany.objects.filter(
            #         id=request.user.company.id
            #     )
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    pass


@admin.register(AgreementDocument)
class AgreementDocumentAdmin(admin.ModelAdmin):
    readonly_fields = ("insurance_company", "insurance_agent")

    def save_model(self, request, obj, form, change):
        if obj:
            obj.insurance_agent = request.user
            if request.user.company:
                obj.insurance_company_id = request.user.company.id
        super().save_model(request, obj, form, change)


@admin.register(CarRepairCompanyOffer)
class CarRepairCompanyOfferAdmin(admin.ModelAdmin):
    list_display = (
        "offer_owner",
        "offer_owner_agent",
        "accident_bidding",
        "accepted_offer",
        "rejected_offer",
    )
    list_filter = (
        # AccidentBiddingFilter,
        "offer_owner__name",
        "offer_owner_agent",
        "accepted_offer",
        "rejected_offer",
        "accident_bidding__accident",
    )

    def save_model(self, request, obj, form, change):
        if obj.accepted_offer and obj.rejected_offer:
            raise ValidationError(
                {
                    "error": "Accepted offer and Rejected offer fields cannot be True at the same time."
                }
            )
        super().save_model(request, obj, form, change)

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        if request.user.is_staff and not request.user.is_superuser:
            if request.user.user_type == "3":  # Assuming '3' represents Insurance Agent
                # Get the insurance policies associated with the Insurance Agent's company
                insurance_policies = InsurancePolicy.objects.filter(
                    insurance_company=request.user.company
                )
                # Get the Customer users associated with these insurance policies
                queryset = CarRepairCompanyOffer.objects.filter(
                    accident_bidding__insurance_company=request.user.company
                )

            return queryset.distinct()
        return queryset

    def get_readonly_fields(self, request, obj=None):
        readonly = list(super().get_readonly_fields(request, obj=obj))
        if not request.user.is_superuser:
            readonly += [
                "offer_owner",
                "offer_owner_agent",
                "accident_bidding",
                "services_to_provide",
                "repair_start_date",
                "repair_start_date",
                "approximate_budget",
                "approximate_duration",
            ]
        return readonly


@admin.register(OfferedServices)
class OfferedServicesAdmin(admin.ModelAdmin):
    pass
