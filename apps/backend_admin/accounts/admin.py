# accounts/admin.py
from django.contrib import admin
from accounts.models import Role


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ["name", "can_upload", "can_manage_users", "can_view_logs"]
    list_filter = ["can_upload", "can_manage_users"]
    search_fields = ["name"]
