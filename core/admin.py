from typing import Any

from django.contrib import admin
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

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
                ),
            },
        ),
    )
    form = MyUserChangeForm
    list_display = ("username", "is_staff", "user_type")
    list_filter = ("is_staff", "is_superuser", "is_active", "groups")
    ordering = ("-date_joined",)
    filter_horizontal = (
        "groups",
        "user_permissions",
    )

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        if request.user.is_staff and not request.user.is_superuser:
            queryset = queryset.filter(
                user_type="1",
            )
            if request.user.user_type == "3":  # Assuming '3' represents Insurance Agent
                # Get the insurance policies associated with the Insurance Agent's company
                insurance_policies = InsurancePolicy.objects.filter(
                    insurance_company=request.user.company
                )
                # Get the Customer users associated with these insurance policies
                customer_users = User.objects.filter(
                    user_type="1", comp_doc__in=insurance_policies
                )
            return customer_users.distinct()
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

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if not request.user.is_superuser:
            if db_field.name == "customer":
                # Customize the queryset here
                kwargs["queryset"] = CustomerUser.objects.filter(
                    user_type=1, is_active=True
                )
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(Accident)
class AccidentAdmin(admin.ModelAdmin):
    pass


@admin.register(AccidentBidding)
class AccidentBiddingAdmin(admin.ModelAdmin):
    readonly_fields = ("accepted_offers",)

    def accepted_offers(self, obj):
        if obj:
            return obj.repair_offer.filter(accepted_offer=True).first()
        else:
            return ""


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    pass


@admin.register(AgreementDocument)
class AgreementDocumentAdmin(admin.ModelAdmin):
    pass


@admin.register(CarRepairCompanyOffer)
class CarRepairCompanyOfferAdmin(admin.ModelAdmin):
    filter_horizontal = ("services_to_provide",)


@admin.register(OfferedServices)
class OfferedServicesAdmin(admin.ModelAdmin):
    pass
