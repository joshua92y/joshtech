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
            "from_email",
            "to_email",
            "message_stream",
            "sent_at",
            "sent",
            "failure_reason",
        ]
