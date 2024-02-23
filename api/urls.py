from django.urls import path

from . import views

app_name = "api"

urlpatterns = [
    path("login/", views.LoginView.as_view(), name="login"),
    # Knox authentication Logout system
    path("logout/", views.LogoutView.as_view(), name="logout"),
]
