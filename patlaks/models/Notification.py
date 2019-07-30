from django.db import models


class Notification(models.Model):
    title = models.CharField(max_length=255, verbose_name='Başlık', null=True, blank=True)
    body = models.CharField(max_length=10000, verbose_name='Metin', null=True, blank=True)
    is_send = models.BooleanField(null=True, blank=True, default=False)
    to = models.CharField(max_length=1000, blank=True, null=True)
    creationDate = models.DateTimeField(auto_now_add=True, verbose_name='Kayıt Tarihi')
