from django.contrib import admin

from .models import *


@admin.register(UserCustomer)
class UserCustomerAdmin(admin.ModelAdmin):
    pass


@admin.register(UserCompany)
class UserCompanyAdmin(admin.ModelAdmin):
    pass


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
