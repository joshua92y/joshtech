from django.urls import path
from .views import MarkdownPostDetailAPIView

urlpatterns = [
    path("mdx/<slug:slug>/", MarkdownPostDetailAPIView.as_view(), name="markdown-post-detail"),
]
