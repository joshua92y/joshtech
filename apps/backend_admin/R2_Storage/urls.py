# apps\backend_admin\R2_Storage\urls.py
from django.urls import path
from .views import FileMetaCreateAPIView, FileMetaDeleteAPIView, FileMetaPurgeAPIView, FileMetaPendingAPIView, FileMetaRestoreAPIView

urlpatterns = [
    path("files/", FileMetaCreateAPIView.as_view()),
    path("files/<int:pk>/", FileMetaDeleteAPIView.as_view()),
    path("files/<int:pk>/restore/", FileMetaRestoreAPIView.as_view()),
    path("files/deletion-complete/", FileMetaPurgeAPIView.as_view()),
    path("files/deletion-pending/", FileMetaPendingAPIView.as_view()),
]
