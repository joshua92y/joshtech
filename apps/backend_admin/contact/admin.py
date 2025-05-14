# backend_admin/contact/admin.py

from django.contrib import admin
from .models import ContactMessage


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    def short_message(self, obj):
        # 메시지가 50자 이상이면 50자까지만 보여주고 ... 추가
        return obj.message[:50] + "..." if len(obj.message) > 50 else obj.message

    short_message.short_description = "Message"  # admin에서 표시될 컬럼 이름

    list_display = (
        "name",
        "email",
        "created_at",
        "subject",
        "short_message",  # 커스텀 메서드 추가
    )
    list_display_links = list_display  # 모든 컬럼을 클릭 가능하게 설정
    list_filter = ("created_at",)
    search_fields = ("name", "email", "message")
