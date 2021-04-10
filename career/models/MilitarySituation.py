from django.db import models

from career.models.BaseModel import BaseModel


class MilitarySituation(BaseModel):
    keyword = models.CharField(max_length=64)
