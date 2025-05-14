# apps\backend_admin\contact\models.py
from django.db import models

class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()

    sent = models.BooleanField(default=False)
    sent_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    failure_reason = models.TextField(null=True, blank=True)

    # 🔽 Postmark 관련 필드 추가
    from_email = models.EmailField(null=True, blank=True)
    to_email = models.EmailField(null=True, blank=True)
    message_stream = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f"[{self.email}] {self.subject}"