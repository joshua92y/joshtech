# apps/R2_Storage/models.py

from django.db import models
from django.conf import settings
from django.utils import timezone


class FileMeta(models.Model):
    # ✅ 업로드 관련
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    uploaded_from = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        help_text="업로드 요청 위치 (예: web, android, api)",
    )

    key = models.CharField(max_length=512, unique=True)
    filename = models.CharField(max_length=255)
    content_type = models.CharField(max_length=100)
    size = models.PositiveIntegerField()
    uploaded_at = models.DateTimeField()

    # ✅ Soft-delete
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)
    deleted_by = models.CharField(
        max_length=100, default="admin", help_text="삭제 요청 유저"
    )
    deleted_from = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        help_text="삭제 요청 위치 (예: web, fastapi, android)",
    )

    # ✅ Hard-delete
    is_purged = models.BooleanField(default=False)
    purged_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.filename} ({self.user})"
