from django.db import models

from career.models.ForeignLanguage import ForeignLanguage
from career.models.Language import Language


class ForeignLanguageDescription(models.Model):
    foreignLanguage = models.ForeignKey(ForeignLanguage, on_delete=models.CASCADE)
    name = models.CharField(max_length=256)
    language = models.ForeignKey(Language, on_delete=models.CASCADE)
