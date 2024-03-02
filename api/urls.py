from django.urls import path

from .views import (
    AssetListView,
    CaseListView,
    CompetitionListView,
    LoginView,
    LogoutView,
    RegisterView,
)

app_name = "api"

urlpatterns = [
    path("login/", LoginView.as_view(), name="login"),
    # Knox authentication Logout system
    path("logout/", LogoutView.as_view(), name="logout"),
    path("register/", RegisterView.as_view(), name="auth_register"),
    path("asset/", AssetListView.as_view(), name="asset-list"),
    path("case/", CaseListView.as_view(), name="case-list"),
    path("competition/", CompetitionListView.as_view(), name="competition-list"),
]
