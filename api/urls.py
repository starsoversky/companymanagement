from django.urls import path

from .views import (
    AccidentBiddingApiView,
    AccidentListView,
    InsurancePolicyListView,
    LoginView,
    LogoutView,
    OfferedServicesListView,
    OfferListView,
    RegisterView,
    VehicleListView,
)

app_name = "api"

urlpatterns = [
    path("login/", LoginView.as_view(), name="login"),
    # Knox authentication Logout system
    path("logout/", LogoutView.as_view(), name="logout"),
    path("register/", RegisterView.as_view(), name="auth_register"),
    path("vehicle/", VehicleListView.as_view(), name="vehicle-list"),
    path("accident/", AccidentListView.as_view(), name="accident-list"),
    path(
        "accbiddlist/", AccidentBiddingApiView.as_view(), name="accident-bidding-list"
    ),
    path("offer/", OfferListView.as_view(), name="accident-list"),
    path("inpolicy/", InsurancePolicyListView.as_view(), name="insurance-policy-list"),
    path("offservices/", OfferedServicesListView.as_view(), name="offered-list"),
]
