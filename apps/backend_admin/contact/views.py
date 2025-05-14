# apps/backend_admin/contact/views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from contact.models import ContactMessage
from contact.serializers import ContactMessageSerializer


class ContactAPIView(APIView):
    """
    문의 메일에 대한 유효성 검사 및 저장 처리 뷰
    """

    def post(self, request):
        serializer = ContactMessageSerializer(data=request.data)
        if serializer.is_valid():
            # 유효성 검증만 하고 저장은 하지 않음
            return Response({"detail": "Validation success."}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class ContactSaveAPIView(APIView):
    def post(self, request):
        serializer = ContactMessageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"detail": "Message saved successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)