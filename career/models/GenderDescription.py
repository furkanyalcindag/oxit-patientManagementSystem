from django.db import models

from career.models.Language import Language
from career.models.Gender import Gender
from career.models.BaseModel import BaseModel


class GenderDescription(BaseModel):
    name = models.CharField(max_length=64)
    gender = models.ForeignKey(Gender, on_delete=models.CASCADE)
    language = models.ForeignKey(Language, on_delete=models.CASCADE)
