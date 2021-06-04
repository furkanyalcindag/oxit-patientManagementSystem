from django.db import models

from pms.models.BaseModel import BaseModel


class Hospital(BaseModel):
    name = models.CharField(max_length=128)