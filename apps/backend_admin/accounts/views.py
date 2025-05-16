# apps/accounts/views.py

from django.contrib.auth import authenticate, get_user_model
from django.utils import timezone
import logging
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

from accounts.token import issue_device_jwt, get_active_device_count_and_list
from accounts.models import UserDeviceToken
from accounts.serializers import CustomTokenRefreshSerializer
from accounts.utils.auth import validate_token_and_device
from config.settings import MAX_DEVICE_COUNT

User = get_user_model()
logger = logging.getLogger(__name__)


class CustomTokenRefreshView(TokenRefreshView):
    """
    POST: JWT 리프레시 토큰을 이용하여 새로운 액세스 토큰 발급

    기존 RefreshToken의 커스텀 클레임(uuid, user_id 등)을 포함하여 AccessToken을 반환합니다.
    """

    serializer_class = CustomTokenRefreshSerializer


class LoginView(APIView):
    """
    POST: 사용자 로그인 및 디바이스 기반 JWT 토큰 발급

    - username, password, device_name을 받아 인증 수행
    - 유효할 경우 access, refresh, uuid를 포함한 토큰 정보 반환
    - 등록된 디바이스가 MAX_DEVICE_COUNT를 초과하면 403 반환
    """

    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        device_name = request.data.get("device_name", "unknown")

        user = authenticate(request, username=username, password=password)
        if not user:
            return Response(
                {"detail": "인증 실패"}, status=status.HTTP_401_UNAUTHORIZED
            )

        # ✅ 토큰 발급 및 등록 (디바이스 수 초과 시 내부에서 처리)
        token_data = issue_device_jwt(user, device_name=device_name)
        if token_data is None:
            device_count, device_list = get_active_device_count_and_list(user)
            return Response(
                {
                    "error": f"디바이스는 최대 {MAX_DEVICE_COUNT}개까지 허용됩니다.",
                    "active_devices": device_list,
                },
                status=status.HTTP_403_FORBIDDEN,
            )
        return Response(token_data, status=status.HTTP_200_OK)


class TokenVerifyView(APIView):
    """
    GET: 전달된 AccessToken 및 uuid를 검증하고 사용자 정보 반환

    - 유효한 경우 사용자 ID, username, 디바이스 uuid, role 정보 포함
    - 잘못된 토큰 또는 uuid는 401 에러 반환
    """

    permission_classes = [AllowAny]

    def get(self, request):
        try:
            user_id, uuid, _ = validate_token_and_device(request)

            # 최근 사용 갱신
            UserDeviceToken.objects.filter(user_id=user_id, uuid=uuid).update(
                last_used_at=timezone.now()
            )

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
            return Response({"detail": str(e)}, status=401)


class LogoutDeviceView(APIView):
    """
    POST: 현재 인증된 사용자의 특정 디바이스 로그아웃

    - uuid를 기반으로 해당 디바이스의 JWT를 블랙리스트 처리하고 비활성화
    - 유효하지 않은 uuid는 404 반환
    """

    permission_classes = [IsAuthenticated]

    def post(self, request):
        uuid = request.data.get("uuid")
        if not uuid or str(uuid).strip() == "":
            return Response({"detail": "유효한 uuid가 필요합니다."}, status=400)

        try:
            device_token = UserDeviceToken.objects.get(
                user=request.user, uuid=uuid, is_active=True
            )

            try:
                outstanding = OutstandingToken.objects.get(jti=device_token.jti)
                BlacklistedToken.objects.get_or_create(token=outstanding)
            except OutstandingToken.DoesNotExist:
                logger.warning(f"토큰이 이미 만료되었거나 존재하지 않음: {uuid}")

            device_token.is_active = False
            device_token.save()

            return Response(
                {"detail": "해당 디바이스에서 로그아웃되었습니다."}, status=200
            )

        except UserDeviceToken.DoesNotExist:
            return Response({"detail": "해당 디바이스를 찾을 수 없습니다."}, status=404)


class DeviceListView(APIView):
    """
    GET: 현재 사용 중인 디바이스 정보 조회

    - AccessToken 및 uuid를 검증하여 단일 디바이스 정보를 반환
    - 디바이스 uuid, 이름, 마지막 사용 시간 포함
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            _, _, device = validate_token_and_device(request)

            return Response(
                {
                    "device_count": 1,
                    "devices": [
                        {
                            "uuid": str(device.uuid),
                            "device_name": device.device_name,
                            "last_used_at": device.last_used_at,
                        }
                    ],
                },
                status=200,
            )
        except Exception as e:
            return Response({"detail": str(e)}, status=401)
