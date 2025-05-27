from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import MarkdownPost
from .serializers import MarkdownPostSerializer

class MarkdownPostDetailAPIView(APIView):
    def get(self, request, slug):
        try:
            post = MarkdownPost.objects.get(slug=slug, is_published=True)
        except MarkdownPost.DoesNotExist:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = MarkdownPostSerializer(post)
        return Response(serializer.data)
