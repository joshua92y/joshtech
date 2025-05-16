# apps/accounts/token.py

import uuid
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.token_blacklist.models import (
    BlacklistedToken,
    OutstandingToken,
)
from accounts.models import UserDeviceToken
from config.settings import MAX_DEVICE_COUNT


def issue_device_jwt(user, device_name="unknown"):
    """
    ✅ 디바이스 UUID 발급 + Refresh/Access 토큰 생성
    - 디바이스 수가 초과되면 None 반환
    """
    active_count = UserDeviceToken.objects.filter(user=user, is_active=True).count()
    if active_count >= MAX_DEVICE_COUNT:
        return None  # 호출한 쪽에서 디바이스 리스트와 함께 에러 처리

    device_uuid = uuid.uuid4()
    refresh = RefreshToken.for_user(user)
    refresh["uuid"] = str(device_uuid)

    _store_device_token(
        user=user,
        device_uuid=device_uuid,
        device_name=device_name,
        jti=refresh["jti"],
    )

    return {
        "refresh": str(refresh),
        "access": str(refresh.access_token),
        "uuid": str(device_uuid),
    }


def _store_device_token(user, device_uuid, device_name, jti):
    UserDeviceToken.objects.create(
        user=user,
        uuid=device_uuid,
        device_name=device_name,
        jti=jti,
    )


def get_active_device_count_and_list(user):
    """
    ✅ 현재 유저의 사용 중인 디바이스 목록 (최신순 정렬)
    """
    devices = UserDeviceToken.objects.filter(user=user, is_active=True).order_by(
        "-last_used_at"
    )
    device_list = [
        {
            "uuid": str(d.uuid),
            "device_name": d.device_name,
            "last_used_at": d.last_used_at,
        }
        for d in devices
    ]
    return devices.count(), device_list


def logout_device(user, device_uuid):
    """
    ✅ 단일 디바이스 로그아웃 (토큰 블랙리스트 처리 및 비활성화)
    """
    try:
        device = UserDeviceToken.objects.get(
            user=user, uuid=device_uuid, is_active=True
        )
        _blacklist_token_by_jti(device.jti)
        device.is_active = False
        device.save()
        return True
    except UserDeviceToken.DoesNotExist:
        return False


def _blacklist_token_by_jti(jti):
    """
    ✅ jti 기반으로 RefreshToken을 블랙리스트 처리
    """
    try:
        token = OutstandingToken.objects.get(jti=jti)
        BlacklistedToken.objects.get_or_create(token=token)
    except OutstandingToken.DoesNotExist:
        pass
