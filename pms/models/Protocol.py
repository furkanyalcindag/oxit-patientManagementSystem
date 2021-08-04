from django.db import models

from pms.models import Patient
from pms.models.Assay import Assay
from pms.models.BaseModel import BaseModel


class Protocol(BaseModel):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    assay = models.ForeignKey(Assay, on_delete=models.CASCADE)
    description = models.CharField(max_length=1028)
    barcode = models.CharField(max_length=256)
