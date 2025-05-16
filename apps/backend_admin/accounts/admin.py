# accounts/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from accounts.models import Role, User, UserDeviceToken


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ["name", "can_upload", "can_manage_users", "can_view_logs"]
    list_filter = ["can_upload", "can_manage_users"]
    search_fields = ["name"]


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """
    ✅ 커스텀 User 모델 등록 + 디바이스 토큰 요약 정보 표시
    """

    list_display = (
        "username",
        "email",
        "is_staff",
        "is_superuser",
        "role",
        "device_count",  # 추가됨
        "last_device_activity",  # 추가됨
    )
    list_filter = ("is_staff", "is_superuser", "is_active", "role")
    search_fields = ("username", "email")
    ordering = ("-date_joined",)

    fieldsets = BaseUserAdmin.fieldsets + (("Custom Fields", {"fields": ("role",)}),)
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ("Custom Fields", {"fields": ("role",)}),
    )

    @admin.display(description="디바이스 수")
    def device_count(self, obj):
        return obj.device_tokens.count()

    @admin.display(description="최근 접속")
    def last_device_activity(self, obj):
        latest = obj.device_tokens.order_by("-last_used_at").first()
        return latest.last_used_at if latest else "N/A"


@admin.register(UserDeviceToken)
class UserDeviceTokenAdmin(admin.ModelAdmin):
    """
    ✅ 디바이스 토큰 모델 등록
    """

    list_display = (
        "user",
        "device_name",
        "uuid",
        "is_active",
        "created_at",
        "last_used_at",
    )
    list_filter = ("is_active", "created_at")
    search_fields = ("user__username", "device_name", "uuid")
    ordering = ("-created_at",)
