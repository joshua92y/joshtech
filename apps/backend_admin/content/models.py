# apps/backend_admin/content/models.py
from django.db import models
from django.conf import settings
from django.utils.text import slugify
from django.utils import timezone
from django_json_widget.widgets import JSONEditorWidget

formfield_overrides = {
    models.JSONField: {'widget': JSONEditorWidget(mode='code', height='300px')}
}

class MarkdownPost(models.Model):
    CONTENT_TYPES = [
        ('work', 'Work'),
        ('project', 'Project'),
        ('post', 'Post'),
        ('page', 'Page'),
    ]
    # ✅ 콘텐츠 및 메타정보
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    summary = models.TextField(blank=True, help_text="간단한 요약")
    content = models.TextField(help_text="마크다운 본문")
    content_type =models.CharField(max_length=10, choices=CONTENT_TYPES)

    # ✅ 이미지, 링크, 태그
    image = models.URLField(blank=True, null=True, help_text="대표 이미지")
    images = models.JSONField(
        blank=True,
        null=True,
        default=list,
        help_text="이미지 경로 배열"
    )
    tag = models.CharField(max_length=50, blank=True, help_text="단일 태그")  # ✅ 단일 문자열로 수정
    link = models.URLField(blank=True, null=True, help_text="관련 링크")

    # ✅ 팀 정보
    team = models.JSONField(blank=True, null=True, default=list, help_text="""
        예: [{"name": "홍길동", "role": "디자이너", "avatar": "/img.png", "linkedIn": "..."}]
    """)

    # ✅ 작성자 및 상태
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    is_published = models.BooleanField(default=False)
    published_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # ✅ 자동 슬러그 및 게시일
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        if self.is_published and not self.published_at:
            self.published_at = timezone.now()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
