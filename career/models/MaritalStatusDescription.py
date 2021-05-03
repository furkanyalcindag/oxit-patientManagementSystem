from django.db import models

from career.models.Language import Language
from career.models.MaritalStatus import MaritalStatus
from career.models.BaseModel import BaseModel


class MaritalStatusDescription(BaseModel):
    maritalStatus = models.ForeignKey(MaritalStatus, on_delete=models.CASCADE)
    language = models.ForeignKey(Language, on_delete=models.CASCADE)
    name = models.CharField(max_length=128)