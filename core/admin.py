from django.contrib import admin
from django.contrib.auth import get_user_model

from .models import *

User = get_user_model()


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_filter = ("user_type",)


@admin.register(CompanyA)
class CompanyAAdmin(admin.ModelAdmin):
    pass


@admin.register(CompanyB)
class CompanyBAdmin(admin.ModelAdmin):
    pass


@admin.register(CompanyDocument)
class CompanyDocumentAdmin(admin.ModelAdmin):
    pass


@admin.register(Asset)
class AssetAdmin(admin.ModelAdmin):
    pass


@admin.register(Case)
class CaseAdmin(admin.ModelAdmin):
    pass


@admin.register(Competition)
class CompetitionAdmin(admin.ModelAdmin):
    pass


@admin.register(Meeting)
class MeetingAdmin(admin.ModelAdmin):
    pass


@admin.register(AgreementDocument)
class AgreementDocumentAdmin(admin.ModelAdmin):
    pass


@admin.register(CompanyOffer)
class CompanyOfferAdmin(admin.ModelAdmin):
    pass
