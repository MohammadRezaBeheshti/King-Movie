from django.urls import path

from .views import (
    UserLoginView,
    UserLogoutView,
    UserRegisterView,
    # profile_view,
)

app_name = "accounts"

urlpatterns = [
    path("login/", UserLoginView.as_view(), name="login"),
    path("register/", UserRegisterView.as_view(), name="register"),
    path("logout/", UserLogoutView.as_view(), name="logout"),
    # path("profile/", profile_view, name="profile"),
]