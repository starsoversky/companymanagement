from django.contrib import admin
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

# from .forms import CarInsuranceDocumentAdminForm
from .models import *

User = get_user_model()


@admin.register(User)
class MyUserAdmin(admin.ModelAdmin):
    readonly_fields = ("company",)
    # fieldsets = (
    #     (None, {"fields": ("email", "password")}),
    #     (
    #         "Personal Info",
    #         {"fields": ("first_name", "last_name", "address", "phone_number")},
    #     ),
    #     (
    #         "Permissions",
    #         {
    #             "fields": (
    #                 "is_active",
    #                 "is_staff",
    #                 "is_blocked",
    #                 "is_admin",
    #                 "groups",
    #                 "user_permissions",
    #             )
    #         },
    #     ),
    #     ("Important dates", {"fields": ("last_login", "date_joined")}),
    # )
    # add_fieldsets = (
    #     (
    #         None,
    #         {
    #             "classes": ("wide",),
    #             "fields": ("email", "password1", "password2"),
    #         },
    #     ),
    # )
    # search_fields = ("email", "first_name", "last_name")
    # ordering = ("email",)


@admin.register(InsuranceCompany)
class InsuranceCompanyAdmin(admin.ModelAdmin):
    pass


@admin.register(CarRepairCompany)
class CarRepairCompanyAdmin(admin.ModelAdmin):
    readonly_fields = ("registration_date",)


@admin.register(InsurancePolicy)
class InsurancePolicyAdmin(admin.ModelAdmin):
    pass


@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    pass


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
