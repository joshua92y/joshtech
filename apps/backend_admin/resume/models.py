from django.db import models

class Resume(models.Model):
    name = models.CharField(max_length=100) # 이름
    email = models.EmailField() # 이메일
    phone = models.CharField(max_length=20) #폰
    summary = models.TextField() #서머리
    created_at = models.DateTimeField(auto_now_add=True) #시간

    def __str__(self):
        return self.name