from django.db import models


class Language(models.Model):
    name = models.CharField(max_length=64)
    code = models.CharField(max_length=12)
    flag = models.TextField(null=True)
