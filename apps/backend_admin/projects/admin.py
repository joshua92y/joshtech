# backend_admin/project/admin.py

from django.contrib import admin
from .models import Project


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "description", "link", "created_at")
    search_fields = ("title", "description")
    list_filter = ("created_at",)
