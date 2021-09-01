from django.db import models

from pms.models.Patient import Patient
from pms.models.BaseModel import BaseModel
from pms.models.Staff import Staff


class Answer(BaseModel):
    description = models.CharField(max_length=2556)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, null=True, blank=True)
    doctor = models.ForeignKey(Staff, on_delete=models.CASCADE, null=True, blank=True)
