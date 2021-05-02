from django.db import models

from career.models.Language import Language
from career.models.ForeignLanguage import ForeignLanguage
from career.models.BaseModel import BaseModel


class ForeignLanguageDescription(BaseModel):
    foreignLanguage = models.ForeignKey(ForeignLanguage, on_delete=models.CASCADE)
    name = models.CharField(max_length=128)
    language = models.ForeignKey(Language, on_delete=models.CASCADE)
