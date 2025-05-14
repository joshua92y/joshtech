# apps\backend_admin\config\urls.py
from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse


def health_check(request):
    return JsonResponse({"status": "ok"})


def crash_test(request):
    division_by_zero = 1 / 0  # 일부러 에러


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/resume/", include("resume.urls")),
    path("api/contact/", include("contact.urls")),
    path("healthz/", health_check, name="health_check"),
    path("sentry-debug/", crash_test, name="crash_test"),
]
