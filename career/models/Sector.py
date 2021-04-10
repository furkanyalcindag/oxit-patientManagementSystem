import uuid as uuid
from django.db import models

from career.models.BaseModel import BaseModel


class Sector(BaseModel):
    name = models.CharField(max_length=128, null=True, blank=True)
