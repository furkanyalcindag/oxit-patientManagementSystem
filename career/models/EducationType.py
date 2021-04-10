from django.db import models

from career.models.BaseModel import BaseModel


class EducationType(BaseModel):
    name = models.CharField(max_length=64, null=True, blank=True)
