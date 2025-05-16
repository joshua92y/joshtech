# apps/accounts/signals.py

"""
accounts/signals.py

📡 역할(Role) 변경 또는 삭제 시, 해당 역할을 사용하는 사용자(user)의 FastAPI 캐시 무효화를 트리거합니다.
- `post_save`, `post_delete` 시그널을 통해 Role 변경 감지
- FastAPI로 user_id를 전달하여 Redis 등에서 캐시 제거
"""

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from accounts.models import Role, User
import requests
from django.conf import settings


def notify_fastapi_invalidate(user_id):
    """
    FastAPI 서버에 사용자 캐시 무효화 요청 전송

    Args:
        user_id (int): 캐시를 무효화할 대상 사용자 ID

    외부 FastAPI API 엔드포인트로 POST 요청을 보내 캐시를 제거합니다.
    실패 시 예외를 잡아 로깅 또는 재시도 큐에 넣도록 설계되어야 합니다.
    """
    try:
        requests.post(
            settings.FASTAPI_CACHE_INVALIDATE_URL,  # e.g., "https://fastapi.internal/api/internal/cache-invalidate/"
            json={"user_id": user_id},
            headers={"Authorization": f"Bearer {settings.INTERNAL_API_KEY}"},
        )
    except requests.RequestException as e:
        # TODO: 로깅 또는 실패 시 재시도 큐에 넣기
        print(f"[CACHE INVALIDATE FAIL] user_id={user_id} - {e}")


@receiver([post_save, post_delete], sender=Role)
def invalidate_users_of_role(sender, instance, **kwargs):
    """
    Role 모델의 변경(post_save) 또는 삭제(post_delete) 시 해당 역할을 사용하는 모든 사용자에 대해 캐시 무효화 요청 전송

    Args:
        sender: 시그널을 보낸 모델 클래스 (Role)
        instance: 변경 또는 삭제된 Role 인스턴스

    동작:
        - Role을 사용하는 모든 User를 조회하여 notify_fastapi_invalidate 호출
        - 결과적으로 FastAPI에 사용자별 캐시 무효화 요청을 보냄
    """
    users = User.objects.filter(role=instance)
    for user in users:
        notify_fastapi_invalidate(user.id)
