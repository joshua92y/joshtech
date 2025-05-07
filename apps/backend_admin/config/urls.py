#apps\backend_admin\config\urls.py
from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/resume/", include("resume.urls")),
    path("api/contact/", include("contact.urls")),
]