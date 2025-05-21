from django.contrib import admin
from .models import FileMeta


@admin.register(FileMeta)
class FileMetaAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "filename",
        "user",
        "is_deleted",
        "is_purged",
        "uploaded_at",
        "deleted_at",
        "deleted_by",
        "deleted_from",
        "purged_at",
        "restored_at",
        "restored_by",
        "restored_from",
        "uploaded_from",
    )
    list_filter = ("is_deleted", "is_purged", "uploaded_from")
    search_fields = ("filename", "key", "user__username")
    ordering = ("-uploaded_at",)
