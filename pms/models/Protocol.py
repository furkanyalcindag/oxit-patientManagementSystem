from django.db import models

from pms.models.Patient import Patient
from pms.models.Assay import Assay
from pms.models.BaseModel import BaseModel


class Protocol(BaseModel):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    description = models.CharField(max_length=1028)
    barcode = models.CharField(max_length=256)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    isPaid = models.BooleanField(default=False)
