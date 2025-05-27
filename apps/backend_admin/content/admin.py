# apps/backend_admin/content/admin.py
from django.contrib import admin
from django.utils.safestring import mark_safe
import json
from .models import MarkdownPost


@admin.register(MarkdownPost)
class MarkdownPostAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "is_published", "tag", "published_at", "created_at")
    list_filter = ("is_published", "tag")
    search_fields = ("title", "summary", "content", "tag")
    readonly_fields = ("slug", "created_at", "updated_at", "formatted_images", "formatted_team")

    fieldsets = (
        ("기본 정보", {
            "fields": ("title", "slug", "summary", "content", "tag", "author")
        }),
        ("미디어", {
            "fields": ("image", "formatted_images","images")
        }),
        ("링크 및 팀", {
            "fields": ("link", "formatted_team","team")
        }),
        ("게시 상태", {
            "fields": ("is_published", "published_at", "created_at", "updated_at")
        }),
    )

    def formatted_images(self, obj):
        if not obj.images:
            return "-"
        try:
            html = "<ul>" + "".join(f"<li>{img}</li>" for img in obj.images) + "</ul>"
            return mark_safe(html)
        except Exception:
            return str(obj.images)
    formatted_images.short_description = "이미지 리스트"

    def formatted_team(self, obj):
        if not obj.team:
            return "-"
        try:
            pretty = json.dumps(obj.team, indent=2, ensure_ascii=False)
            return mark_safe(f"<pre style='white-space: pre-wrap'>{pretty}</pre>")
        except Exception:
            return str(obj.team)
    formatted_team.short_description = "팀 정보 (JSON)"
