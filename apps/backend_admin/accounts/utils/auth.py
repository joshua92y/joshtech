# accounts/utils/auth.py
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.exceptions import AuthenticationFailed
from accounts.models import UserDeviceToken


def validate_token_and_device(request):
    """
    ✅ AccessToken에서 uuid, user_id 추출 및 해당 디바이스 유효성 검사
    - 실패 시 AuthenticationFailed 예외 발생
    - 성공 시 (user_id, uuid, device 객체) 반환
    """
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise AuthenticationFailed("Authorization 헤더 누락")

    token_str = auth_header.removeprefix("Bearer ").strip()

    try:
        token = AccessToken(token_str)
        uuid = token.get("uuid")
        user_id = token.get("user_id") or token.get("sub")

        if not uuid or not user_id:
            raise AuthenticationFailed("토큰 정보가 유효하지 않습니다.")

        try:
            device = UserDeviceToken.objects.get(
                user_id=user_id, uuid=uuid, is_active=True
            )
        except UserDeviceToken.DoesNotExist:
            raise AuthenticationFailed("UUID 인증 실패")

        return user_id, uuid, device

    except Exception as e:
        raise AuthenticationFailed(f"토큰 파싱 오류: {e}")
