from django.db import models

from booqe.models import Profile
from booqe.models.Blog import Blog


class PinnedBlog(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, default=None)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, default=None)
    creationDate = models.DateTimeField(auto_now_add=True, verbose_name='Kayıt Tarihi')
