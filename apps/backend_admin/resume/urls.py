from django.urls import path
from .views import ResumeAPIView

urlpatterns = [
    path("", ResumeAPIView.as_view(), name="resume-create"),
]
