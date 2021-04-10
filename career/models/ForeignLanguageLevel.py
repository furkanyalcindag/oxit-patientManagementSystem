from django.db import models


class ForeignLanguageLevel(models.Model):
    name = models.CharField(max_length=128)
