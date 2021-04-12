from django.db import models

from career.models.BaseModel import BaseModel


class City(BaseModel):
    name = models.CharField(max_length=64)
