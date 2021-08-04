from django.db import models

from pms.models.BaseModel import BaseModel


class Assay(BaseModel):
    name = models.CharField(max_length=256)
