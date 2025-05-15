import uuid
from rest_framework_simplejwt.serializers import (
    TokenObtainPairSerializer,
    TokenRefreshSerializer,
)
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from accounts.models import UserDeviceToken
from accounts.token import (
    _remove_oldest_device_if_limit_exceeded,
    _store_device_token,
)


class DeviceTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    ✅ 로그인 시: 디바이스 UUID + JWT 토큰 발급 + DB 저장
    """

    def validate(self, attrs):
        data = super().validate(attrs)

        user = self.user
        device_name = self.context["request"].data.get("device_name", "unknown")
        device_uuid = uuid.uuid4()

        # 1️⃣ Refresh 토큰 생성 + UUID 클레임 포함
        refresh = RefreshToken.for_user(user)
        refresh["uuid"] = str(device_uuid)

        # 2️⃣ 디바이스 수 제한 검사 + 저장
        _remove_oldest_device_if_limit_exceeded(user)
        _store_device_token(
            user=user,
            device_uuid=device_uuid,
            device_name=device_name,
            jti=refresh["jti"],
        )

        # 3️⃣ 응답 반환
        data["refresh"] = str(refresh)
        data["access"] = str(refresh.access_token)
        data["uuid"] = str(device_uuid)
        return data


class CustomTokenRefreshSerializer(TokenRefreshSerializer):
    """
    ✅ Refresh 시: 원래 RefreshToken의 커스텀 클레임(uuid 등)을 복사하여 AccessToken 생성
    """

    def validate(self, attrs):
        # 기본 검증 수행 → refresh 유효성 + 만료 검사
        data = super().validate(attrs)

        # 기존 refresh 토큰 파싱
        refresh = RefreshToken(attrs["refresh"])

        # Access 토큰 생성 + 커스텀 클레임 복사
        access = refresh.access_token
        access["uuid"] = refresh.get("uuid")
        access["user_id"] = refresh.get("user_id")

        data["access"] = str(access)
        return data
