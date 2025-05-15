# apps/accounts/models.py

import uuid
from django.db import models
from django.conf import settings
from django.utils import timezone
from django.contrib.auth.models import AbstractUser


class UserDeviceToken(models.Model):
    """
    ✅ 유저의 디바이스 및 해당 JWT 토큰 정보 추적
    """

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="device_tokens"
    )
    uuid = models.UUIDField(default=uuid.uuid4, unique=True)  # 디바이스 고유 식별자
    jti = models.CharField(max_length=255, unique=True)  # JWT 고유 ID (refresh용)
    device_name = models.CharField(
        max_length=100, null=True, blank=True
    )  # ex: "Chrome on Windows"
    created_at = models.DateTimeField(default=timezone.now)
    last_used_at = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together = ("user", "uuid")  # 1 유저 1 디바이스 1 UUID
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user.username} - {self.device_name or 'device'} ({self.uuid})"


class Role(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)

    # ✅ 기능 권한 예시 필드
    can_upload = models.BooleanField(default=False)
    can_view_logs = models.BooleanField(default=False)
    can_manage_users = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class User(AbstractUser):
    role = models.ForeignKey(
        "accounts.Role",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="users",
    )

    def has_permission(self, permission_name):
        if not self.role:
            return False
        return getattr(self.role, permission_name, False)
