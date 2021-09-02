from django.db import models

from pms.models.Patient import Patient
from pms.models.BaseModel import BaseModel


class Question(BaseModel):
    description = models.CharField(max_length=2556)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
