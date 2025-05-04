from rest_framework.views import APIView  # DRF의 기본 API 뷰 클래스
from rest_framework.response import Response  # JSON 응답을 위한 클래스
from rest_framework import status  # HTTP 상태 코드 정의
from .forms import ResumeForm  #Form
from .models import Resume  # (선택) Resume 모델 import (디버깅용 등)

class ResumeAPIView(APIView):
    """
    이력서 제출을 처리하는 POST API
    - 클라이언트에서 전송한 JSON 데이터를 Form으로 검증
    - 검증 통과 시 DB에 저장
    - 성공/실패 여부에 따라 JSON 응답 반환
    """

    def post(self, request, *args, **kwargs):
        # ✅ 클라이언트에서 전송한 JSON 데이터를 기반으로 Form 생성
        form = ResumeForm(data=request.data)

        # ✅ 유효성 검사 통과 시
        if form.is_valid():
            # DB에 저장하고 저장된 객체 반환
            resume = form.save()

            # 성공 응답 (201 Created)
            return Response({
                "id": resume.id,
                "message": "Resume submitted successfully"
            }, status=status.HTTP_201_CREATED)

        # ❌ 유효성 검사 실패 시, 에러 메시지를 포함한 400 응답 반환
        return Response({
            "errors": form.errors  # 어떤 필드가 왜 잘못됐는지 상세 정보 포함
        }, status=status.HTTP_400_BAD_REQUEST)
