from django.db import models

from booqe.models import Blog, Profile


class Comment(models.Model):

    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    whoComment = models.ForeignKey(Profile, on_delete=models.CASCADE)
    comment = models.TextField(blank=True, null=True)
    creationDate = models.DateTimeField(auto_now_add=True, verbose_name='Kayıt Tarihi')