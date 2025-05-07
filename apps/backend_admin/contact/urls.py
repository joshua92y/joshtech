# apps/backend_admin/contact/urls.py
from django.urls import path
from .views import ContactAPIView, ContactSaveAPIView

urlpatterns = [
    path("validate/", ContactAPIView.as_view(), name="contact-validate"),
    path("save/", ContactSaveAPIView.as_view(), name="contact-save"),
]
