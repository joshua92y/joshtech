# apps/accounts/serializers.py

from rest_framework_simplejwt.serializers import (
    TokenObtainPairSerializer,
    TokenRefreshSerializer,
)
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import serializers

from accounts.token import issue_device_jwt, get_active_device_count_and_list
from config.settings import MAX_DEVICE_COUNT


class DeviceTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    ✅ 로그인 시: 디바이스 UUID + JWT 토큰 발급 + DB 저장
    """

    def validate(self, attrs):
        data = super().validate(attrs)
        user = self.user
        device_name = self.context["request"].data.get("device_name", "unknown")

        token_data = issue_device_jwt(user, device_name)
        if token_data is None:
            device_count, device_list = get_active_device_count_and_list(user)
            raise serializers.ValidationError(
                {
                    "error": f"디바이스는 최대 {MAX_DEVICE_COUNT}개까지 허용됩니다.",
                    "active_devices": device_list,
                }
            )

        data.update(token_data)
        return data


class CustomTokenRefreshSerializer(TokenRefreshSerializer):
    """
    ✅ Refresh 시: 기존 RefreshToken의 커스텀 클레임(uuid 등)을 복사하여 AccessToken 생성
    """

    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = RefreshToken(attrs["refresh"])

        access = refresh.access_token
        access["uuid"] = refresh.get("uuid")
        access["user_id"] = refresh.get("user_id")  # optional

        data["access"] = str(access)
        return data
