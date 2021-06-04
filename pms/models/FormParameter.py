from django.db import models

from pms.models.BaseModel import BaseModel


class FormParameter(BaseModel):
    name = models.CharField(max_length=128)
    type = models.CharField(max_length=128)





