from django.db import models

from career.models.BaseModel import BaseModel


class MaritalStatus(BaseModel):
    keyword = models.CharField(max_length=56, null=True)
