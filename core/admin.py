from django.contrib import admin
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.contrib.auth import get_user_model

from .forms import CarInsuranceDocumentAdminForm
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
    pass


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    pass


@admin.register(AgreementDocument)
class AgreementDocumentAdmin(admin.ModelAdmin):
    pass


@admin.register(CarInsuranceDocument)
class CarInsuranceDocumentAdmin(admin.ModelAdmin):
    filter_horizontal = ("services_to_provide",)


@admin.register(ServicesProvide)
class ServicesProvideAdmin(admin.ModelAdmin):
    pass
