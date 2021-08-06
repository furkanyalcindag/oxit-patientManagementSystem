from django.db import models

from pms.models.Patient import Patient
from pms.models.Assay import Assay
from pms.models.BaseModel import BaseModel


class AssayResult(BaseModel):
    assay = models.ForeignKey(Assay, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    result = models.CharField(max_length=256)
