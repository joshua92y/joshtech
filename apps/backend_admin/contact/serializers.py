# apps/backend_admin/contact/serializers.py

from rest_framework import serializers
from contact.models import ContactMessage


class ContactMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactMessage
        fields = [
            "name",
            "email",
            "subject",
            "message",
        ]
