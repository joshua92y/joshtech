# apps/accounts/serializers.py

from rest_framework_simplejwt.serializers import (
    TokenObtainPairSerializer,
    TokenRefreshSerializer,
)
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import serializers

from accounts.token import issue_device_jwt, get_active_device_count_and_list
from config.settings import MAX_DEVICE_COUNT

from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password


UserModel = get_user_model()


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


class RegisterSerializer(serializers.ModelSerializer):
    """
    ✅ 사용자 회원가입용 시리얼라이저 (FastAPI ↔ Django 스키마 호환)

    - FastAPI에서 전달받은 회원가입 데이터(username, email, password, role)를 검증 및 처리
    - Django의 User 모델과 연동되어 .save() 시 create_user()를 호출해 저장
    - Pydantic 기반 shared_schemas.User 모델과 필드 구조 일치
    - 비밀번호는 write_only로 설정되고 Django의 비밀번호 유효성 검증기를 사용함
    """

    password = serializers.CharField(write_only=True, validators=[validate_password])

    class Meta:
        model = UserModel
        fields = ["username", "email", "password", "role"]  # shared 스키마와 일치
        extra_kwargs = {
            "email": {"required": True},
            "role": {"required": False},
        }

    def create(self, validated_data):
        return UserModel.objects.create_user(**validated_data)
