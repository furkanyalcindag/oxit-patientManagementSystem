from django.db import models

from booqe.models import Profile, Blog


class Like(models.Model):

    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    whoLike = models.ForeignKey(Profile, on_delete=models.CASCADE)
    isDelete = models.BooleanField(default=False)
    creationDate = models.DateTimeField(auto_now_add=True, verbose_name='Kayıt Tarihi')
    modificationDate = models.DateTimeField(auto_now=True, verbose_name='Güncelleme Tarihi')


