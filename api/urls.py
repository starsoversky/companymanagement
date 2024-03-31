from django.urls import path

from .views import (
    AccidentBiddingApiView,
    AccidentDetailView,
    AccidentListView,
    AgreementDocumentListView,
    AppointmentListView,
    InsurancePolicyListView,
    LoginView,
    LogoutView,
    OfferDetailView,
    OfferedServicesListView,
    OfferListView,
    RegisterView,
    VehicleDetailView,
    VehicleListView,
)

app_name = "api"

urlpatterns = [
    path("login/", LoginView.as_view(), name="login"),
    # Knox authentication Logout system
    path("logout/", LogoutView.as_view(), name="logout"),
    path("register/", RegisterView.as_view(), name="auth_register"),
    path("vehicle/", VehicleListView.as_view(), name="vehicle-list"),
    path("vehicle/<int:pk>/", VehicleDetailView.as_view(), name="vehicle-detail"),
    path("accident/", AccidentListView.as_view(), name="accident-list"),
    path("accident/<int:pk>/", AccidentDetailView.as_view(), name="accident-detail"),
    path(
        "accbiddlist/", AccidentBiddingApiView.as_view(), name="accident-bidding-list"
    ),
    path("offer/", OfferListView.as_view(), name="accident-list"),
    path("offer/<int:pk>/", OfferDetailView.as_view(), name="offer-detail"),
    path("inpolicy/", InsurancePolicyListView.as_view(), name="insurance-policy-list"),
    path("carpolicy/", AgreementDocumentListView.as_view(), name="car-policy-list"),
    path("offservices/", OfferedServicesListView.as_view(), name="offered-list"),
    path("appointment/", AppointmentListView.as_view(), name="appointment-list"),
]
