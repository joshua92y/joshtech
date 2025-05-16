# apps\backend_admin\config\urls.py
from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)


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
# 🧱 Swagger/OpenAPI 문서용
urlpatterns += [
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "api/docs/swagger/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path(
        "api/docs/redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"
    ),
]
