from django.db import models

from pms.models.BaseModel import BaseModel


class Advertising(BaseModel):
    name = models.CharField(max_length=256)
    width = models.CharField(max_length=256)
    height = models.CharField(max_length=256)
    price = models.IntegerField()
