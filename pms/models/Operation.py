from django.db import models

from pms.models.BaseModel import BaseModel
from pms.models.Clinic import Clinic
from pms.models.Hospital import Hospital
from pms.models.Patient import Patient


class Operation(BaseModel):
    name = models.CharField(max_length=128)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE)
    operationDescription = models.TextField(null=True)
    operationDate = models.DateField()
    operationTime = models.TimeField()
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE)
