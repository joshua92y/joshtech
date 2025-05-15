# apps\backend_admin\config\urls.py
from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse


def health_check(request):
    return JsonResponse({"status": "ok"})


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/resume/", include("resume.urls")),
    path("api/contact/", include("contact.urls")),
    path("healthz/", health_check, name="health_check"),
    path("api/files/", include("R2_Storage.urls")),
    path("api/accounts/", include("accounts.urls")),
]
