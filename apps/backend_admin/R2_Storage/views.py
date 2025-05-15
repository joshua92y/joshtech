# apps/R2_Storage/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import FileMetaSerializer
from .models import FileMeta
from django.utils import timezone
from django.contrib.auth import get_user_model

User = get_user_model()


class FileMetaCreateAPIView(APIView):
    def post(self, request):
        data = request.data.copy()

        # 유저 설정: FastAPI에서 user_id 넘기거나 기본 admin 사용
        user_id = data.get("user")
        if not user_id:
            try:
                admin = User.objects.get(username="admin")
                data["user"] = admin.id
            except User.DoesNotExist:
                return Response({"error": "admin 유저 없음"}, status=400)

        if "uploaded_at" not in data:
            data["uploaded_at"] = timezone.now()

        if "uploaded_from" not in data:
            data["uploaded_from"] = "api"

        serializer = FileMetaSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FileMetaDeleteAPIView(APIView):
    def delete(self, request, pk):
        deleted_from = request.query_params.get("from", "admin-panel")
        deleted_by = request.query_params.get("by", "admin")

        try:
            file = FileMeta.objects.get(pk=pk, is_deleted=False)

            file.is_deleted = True
            file.deleted_at = timezone.now()
            file.deleted_by = deleted_by
            file.deleted_from = deleted_from

            file.save(
                update_fields=["is_deleted", "deleted_at", "deleted_by", "deleted_from"]
            )

            return Response({"status": "소프트 삭제 완료"}, status=status.HTTP_200_OK)

        except FileMeta.DoesNotExist:
            return Response(
                {"error": "파일 없음 또는 이미 삭제됨"},
                status=status.HTTP_404_NOT_FOUND,
            )


class FileMetaPurgeAPIView(APIView):
    def post(self, request):
        updates = request.data  # Expects list: [{ id, is_purged, purged_at }]
        updated = 0

        for item in updates:
            pk = item.get("id")
            if not pk:
                continue
            try:
                file = FileMeta.objects.get(id=pk, is_deleted=True, is_purged=False)
                file.is_purged = item.get("is_purged", True)
                file.purged_at = item.get("purged_at", timezone.now())
                file.save(update_fields=["is_purged", "purged_at"])
                updated += 1
            except FileMeta.DoesNotExist:
                continue

        return Response({"updated": updated}, status=status.HTTP_200_OK)
