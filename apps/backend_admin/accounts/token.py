# apps/accounts/token.py

import uuid
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.token_blacklist.models import (
    BlacklistedToken,
    OutstandingToken,
)

from accounts.models import UserDeviceToken

MAX_DEVICE_COUNT = 3


def create_device_token(user, device_name="unknown"):
    """
    ✅ 디바이스 UUID 발급 + Refresh/Access 토큰 생성 및 DB 저장
    """
    device_uuid = uuid.uuid4()
    refresh = RefreshToken.for_user(user)
    refresh["uuid"] = str(device_uuid)

    # 디바이스 토큰 정보 저장
    UserDeviceToken.objects.create(
        user=user,
        uuid=device_uuid,
        device_name=device_name,
        jti=refresh["jti"],
    )

    return {
        "access": str(refresh.access_token),
        "refresh": str(refresh),
        "uuid": str(device_uuid),
    }


def get_active_device_count_and_list(user):
    """
    ✅ 현재 유저의 활성 디바이스 개수와 목록 반환
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
    ✅ 특정 디바이스 UUID에 해당하는 토큰을 블랙리스트 처리하고 soft-delete
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
    내부용: jti 기준으로 RefreshToken을 블랙리스트에 등록
    """
    try:
        token = OutstandingToken.objects.get(jti=jti)
        BlacklistedToken.objects.get_or_create(token=token)
    except OutstandingToken.DoesNotExist:
        pass
