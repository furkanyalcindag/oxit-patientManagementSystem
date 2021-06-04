from django.db import models

from pms.models.BaseModel import BaseModel
from pms.models.Clinic import Clinic
from pms.models.Hospital import Hospital


class ClinicPlan(BaseModel):
    name = models.CharField(max_length=128)
    clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE)
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)