# apps/accounts/urls.py
from django.urls import path
from accounts.views import (
    LoginView,
    TokenVerifyView,
    CustomTokenRefreshView,
    LogoutDeviceView,
    DeviceListView,
)
from accounts.fastapi.registerAPIView import RegisterAPIView

urlpatterns = [
    path("login/", LoginView.as_view(), name="login"),
    path("refresh/", CustomTokenRefreshView.as_view(), name="token_refresh"),
    path("verify/", TokenVerifyView.as_view(), name="token_verify"),
    path("logout/", LogoutDeviceView.as_view(), name="logout_device"),
    path("devices/", DeviceListView.as_view(), name="device_list"),
    path(
        "internal/register/", RegisterAPIView.as_view(), name="register"
    ),  # /api/accounts/internal/register/
]
