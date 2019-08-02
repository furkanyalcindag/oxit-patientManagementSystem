from django.db import models

from patlaks.models import Competitor


class Message(models.Model):
    body = models.CharField(max_length=10000, verbose_name='Mesaj', null=True, blank=True)
    is_send = models.BooleanField(null=True, blank=True, default=False)
    to = models.ForeignKey(Competitor,  on_delete=models.CASCADE)
    creationDate = models.DateTimeField(auto_now_add=True, verbose_name='Kayıt Tarihi')