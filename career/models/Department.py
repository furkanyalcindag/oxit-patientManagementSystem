from django.db import models

from career.models.BaseModel import BaseModel


class Department(BaseModel):
    name = models.CharField(max_length=256, null=True, blank=True)

