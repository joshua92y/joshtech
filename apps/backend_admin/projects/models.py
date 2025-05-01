from django.db import models

class Project(models.Model):
    title = models.CharField(max_length=100) #프로젝트명
    description = models.TextField() #설명
    link = models.URLField(blank=True, null=True) #링크(URL)
    tag = models.CharField(max_length=100,null=True) #태그(tag)
    created_at = models.DateTimeField(auto_now_add=True) #작성시간

    def __str__(self):
        return self.title