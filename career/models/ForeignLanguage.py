from django.db import models


class ForeignLanguage(models.Model):
    keyword = models.CharField(max_length=128)
