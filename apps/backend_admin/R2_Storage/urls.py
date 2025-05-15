from django.urls import path
from .views import FileMetaCreateAPIView, FileMetaDeleteAPIView, FileMetaPurgeAPIView

urlpatterns = [
    path("files/", FileMetaCreateAPIView.as_view()),
    path("files/<int:pk>/", FileMetaDeleteAPIView.as_view()),
    path("files/deletion-complete/", FileMetaPurgeAPIView.as_view()),
]
