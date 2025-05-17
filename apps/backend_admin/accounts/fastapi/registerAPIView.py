# apps/accounts/fastapi/registerAPIView.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from accounts.serializers import RegisterSerializer

# import redis
from django.conf import settings
from django.contrib.auth import get_user_model

User = get_user_model()
# redis_client = redis.Redis.from_url(settings.REDIS_URL)


class RegisterAPIView(APIView):
    """
    ✅ 사용자 회원가입 API

    - FastAPI 또는 프론트엔드에서 전달받은 회원가입 정보를 기반으로
      Django DB에 유저를 생성하는 API
    - 요청 본문은 shared_schemas.User 기반 구조
    - 응답: 201 Created 또는 400 Bad Request
    """

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"detail": "회원가입 성공"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CheckDuplicateUsernameAPIView(APIView):
    """
    ✅ 사용자명 중복 확인 + Redis 캐시 설정
    """

    def get(self, request):
        username = request.query_params.get("username")
        if not username:
            return Response({"error": "username은 필수입니다."}, status=400)

        # DB에서 중복 확인
        if User.objects.filter(username=username).exists():
            return Response(
                {"available": False, "detail": "이미 사용 중인 아이디입니다."}
            )

        # 중복이 아니라면 Redis에 캐시 설정
        # redis_key = f"checked_username:{username}"
        # redis_client.setex(redis_key, 600, "ok")  # 10분간 유효

        return Response({"available": True, "detail": "사용 가능한 아이디입니다."})
