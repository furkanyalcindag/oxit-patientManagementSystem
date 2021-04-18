from django.db import models

from career.models.BaseModel import BaseModel


class Gender(BaseModel):
    keyword = models.CharField(max_length=24, null=True)
