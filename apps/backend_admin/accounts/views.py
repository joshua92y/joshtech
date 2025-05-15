# apps/accounts/views.py

from django.contrib.auth import authenticate, get_user_model
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework_simplejwt.token_blacklist.models import (
    OutstandingToken,
    BlacklistedToken,
)
import requests

from accounts.token import create_device_token, get_active_device_count_and_list
from accounts.models import UserDeviceToken
from accounts.serializers import CustomTokenRefreshSerializer

User = get_user_model()

MAX_DEVICE_COUNT = 3


class CustomTokenRefreshView(TokenRefreshView):
    """
    ✅ RefreshToken → AccessToken 재발급 (uuid, user_id 클레임 유지)
    """

    serializer_class = CustomTokenRefreshSerializer


class LoginView(APIView):
    """
    ✅ 사용자 로그인 + 디바이스 UUID별 토큰 발급 / 디바이스 수 초과 여부 확인
    """

    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        device_name = request.data.get("device_name", "unknown")

        user = authenticate(request, username=username, password=password)
        if not user:
            return Response({"error": "인증 실패"}, status=status.HTTP_401_UNAUTHORIZED)

        # ✅ 디바이스 수 초과 여부 확인
        device_count, device_list = get_active_device_count_and_list(user)
        if device_count >= MAX_DEVICE_COUNT:
            return Response(
                {
                    "error": f"디바이스는 최대 {MAX_DEVICE_COUNT}개까지 허용됩니다.",
                    "active_devices": device_list,
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        # ✅ 토큰 발급 및 등록
        token_data = create_device_token(user, device_name=device_name)
        return Response(token_data, status=status.HTTP_200_OK)


class TokenVerifyView(APIView):
    """
    ✅ AccessToken 검증 + UUID 확인 + Role 정보 포함 반환
    """

    permission_classes = [AllowAny]

    def get(self, request):
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return Response({"detail": "Authorization 헤더 누락"}, status=401)

        token_str = auth_header.removeprefix("Bearer ").strip()

        try:
            token = AccessToken(token_str)
            uuid = token.get("uuid")
            user_id = token.get("user_id") or token.get("sub")

            if not uuid or not user_id:
                return Response({"detail": "유효하지 않은 토큰"}, status=401)

            if not UserDeviceToken.objects.filter(
                user_id=user_id, uuid=uuid, is_active=True
            ).exists():
                return Response({"detail": "UUID 인증 실패"}, status=401)

            user = User.objects.select_related("role").get(id=user_id)
            role = user.role

            role_data = (
                {
                    "name": role.name,
                    "can_upload": role.can_upload,
                    "can_view_logs": role.can_view_logs,
                    "can_manage_users": role.can_manage_users,
                }
                if role
                else None
            )

            return Response(
                {
                    "id": user.id,
                    "username": user.username,
                    "uuid": uuid,
                    "role": role_data,
                },
                status=200,
            )

        except Exception as e:
            return Response(
                {"detail": "토큰 오류", "error": str(e)},
                status=401,
            )


class LogoutDeviceView(APIView):
    """
    ✅ 단일 디바이스 로그아웃 API
    - 주어진 uuid에 해당하는 refresh token을 블랙리스트 처리
    - 해당 디바이스 토큰을 soft-delete 처리 (is_active=False)
    """

    permission_classes = [IsAuthenticated]

    def post(self, request):
        uuid = request.data.get("uuid")
        if not uuid:
            return Response({"detail": "uuid가 필요합니다."}, status=400)

        try:
            # 해당 user와 uuid에 해당하는 디바이스 찾기
            device_token = UserDeviceToken.objects.get(
                user=request.user, uuid=uuid, is_active=True
            )

            # 🔒 토큰 블랙리스트 처리
            try:
                outstanding = OutstandingToken.objects.get(jti=device_token.jti)
                BlacklistedToken.objects.get_or_create(token=outstanding)
            except OutstandingToken.DoesNotExist:
                pass  # 이미 만료된 경우는 무시

            # 💤 Soft-delete 처리
            device_token.is_active = False
            device_token.save()

            return Response(
                {"detail": "해당 디바이스에서 로그아웃되었습니다."}, status=200
            )

        except UserDeviceToken.DoesNotExist:
            return Response({"detail": "해당 디바이스를 찾을 수 없습니다."}, status=404)


def notify_role_update(user_id):
    try:
        requests.post(
            "https://api.yourfastapi.com/internal/cache-invalidate/",
            json={"user_id": user_id},
            headers={"Authorization": f"Bearer {settings.INTERNAL_API_KEY}"},
        )
    except requests.RequestException:
        pass  # 실패 시 재시도 로직 고려
