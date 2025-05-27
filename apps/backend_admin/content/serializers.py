from rest_framework import serializers
from .models import MarkdownPost

class MarkdownPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = MarkdownPost
        fields = ["title", "slug", "content", "author", "published_at"]
