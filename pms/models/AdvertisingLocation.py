from django.db import models

from pms.models.BaseModel import BaseModel


class AdvertisingLocation(BaseModel):
    name = models.CharField(max_length=256)
    width = models.CharField(max_length=256)
    height = models.CharField(max_length=256)
