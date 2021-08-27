from django.db import models


class ProtocolSituation(models.Model):
    name = models.CharField(max_length=128, null=True, blank=True)
