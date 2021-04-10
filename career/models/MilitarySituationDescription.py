from django.db import models

from career.models.BaseModel import BaseModel
from career.models.Language import Language



class MilitarySituationDescription(BaseModel):
    name=models.CharField(max_length=128)
    language=models.ForeignKey(Language, on_delete=models.CASCADE)