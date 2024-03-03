from django.contrib import admin
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.contrib.auth import get_user_model

# from .forms import CarInsuranceDocumentAdminForm
from .models import *

User = get_user_model()


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_filter = ("user_type",)


@admin.register(InsuranceCompany)
class InsuranceCompanyAdmin(admin.ModelAdmin):
    pass


@admin.register(CarRepairCompany)
class CarRepairCompanyAdmin(admin.ModelAdmin):
    pass


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
            return obj.repair_offer.filter(accepted_offer=True)
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
