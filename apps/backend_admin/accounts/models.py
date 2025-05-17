# apps/accounts/models.py

import uuid
from django.db import models
from django.conf import settings
from django.utils import timezone
from django.contrib.auth.models import AbstractUser


class UserDeviceToken(models.Model):
    """
    ✅ 유저의 디바이스 및 JWT 관련 토큰 정보 관리
    - 각 디바이스는 UUID로 식별됨
    - jti는 RefreshToken 재발급 여부 확인용으로 사용
    """

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="device_tokens"
    )
    uuid = models.UUIDField(default=uuid.uuid4, unique=True)  # 디바이스 고유 식별자
    jti = models.CharField(max_length=255, unique=True)  # JWT ID (refresh 식별용)
    device_name = models.CharField(
        max_length=100, null=True, blank=True
    )  # ex: "Chrome on Mac"
    created_at = models.DateTimeField(default=timezone.now)
    last_used_at = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)  # 디바이스 사용 중 여부

    class Meta:
        unique_together = ("user", "uuid")  # 유저별 UUID 1개 제한
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user.username} - {self.device_name or 'device'} ({self.uuid})"


class Role(models.Model):
    """
    ✅ 권한 그룹 역할 정의
    - 각 Role은 여러 유저에게 할당 가능
    """

    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)

    # 💡 권한 예시 필드들 (필요시 추가 확장 가능)
    # can_upload = models.BooleanField(default=False)
    # can_view_logs = models.BooleanField(default=False)
    # can_manage_users = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class User(AbstractUser):
    """
    ✅ 사용자 모델 확장
    - Role 연동을 통해 권한 제어
    """

    role = models.ForeignKey(
        "accounts.Role",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="users",
    )

    def has_permission(self, permission_name: str) -> bool:
        """
        사용자가 특정 권한을 가지고 있는지 확인
        """
        if not self.role:
            return False
        return getattr(self.role, permission_name, False)
