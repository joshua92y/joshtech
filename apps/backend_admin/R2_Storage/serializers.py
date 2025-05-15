from rest_framework import serializers
from .models import FileMeta


class FileMetaSerializer(serializers.ModelSerializer):
    class Meta:
        model = FileMeta
        fields = "__all__"
