from django.contrib import admin

from .models import CarRepairCompanyOffer


class AccidentBiddingFilter(admin.SimpleListFilter):
    title = "Accident Bidding"
    parameter_name = "accident_bidding"

    def lookups(self, request, model_admin):
        accident_biddings = CarRepairCompanyOffer.objects.values_list(
            "accident_biddingid", "accident_biddingname"
        ).distinct()
        return [
            (bidding_id, bidding_name) for bidding_id, bidding_name in accident_biddings
        ]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(accident_bidding__id=self.value())
