from django.db import models

from pms.models.BaseModel import BaseModel


class Branch(BaseModel):
    name = models.CharField(max_length=128, null=True, blank=True)
