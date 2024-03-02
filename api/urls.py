from django.urls import path

from .views import (
    AccidentBiddingListView,
    AccidentListView,
    LoginView,
    LogoutView,
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
    path("acbid/", AccidentBiddingListView.as_view(), name="accident-bidding-list"),
]
