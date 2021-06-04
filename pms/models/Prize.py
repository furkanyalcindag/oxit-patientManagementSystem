from django.db import models

from pms.models.BaseModel import BaseModel
from pms.models.Staff import Staff


class Prize(BaseModel):
    title = models.CharField(max_length=128)
    description = models.CharField(max_length=256)
    date = models.DateField()
    doctor = models.ForeignKey(Staff, on_delete=models.CASCADE)
