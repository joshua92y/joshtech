# backend_admin/contact/admin.py

from django.contrib import admin
from .models import ContactMessage


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "email", "created_at")  # ✅ created_at 추가
    list_filter = ("created_at",)
    search_fields = ("name", "email", "message")
