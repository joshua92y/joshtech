# apps/accounts/signals.py

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from accounts.models import Role, User
import requests
from django.conf import settings


def notify_fastapi_invalidate(user_id):
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
    users = User.objects.filter(role=instance)
    for user in users:
        notify_fastapi_invalidate(user.id)
