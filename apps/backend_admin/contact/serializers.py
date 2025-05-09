from rest_framework import serializers
from contact.models import ContactMessage


class ContactMessageSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(read_only=True)
    sent_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = ContactMessage
        fields = [
            "name",
            "email",
            "subject",
            "message",
            "from_email",
            "to_email",
            "message_stream",
            "created_at",
            "sent_at",
            "sent",
            "failure_reason",
        ]
