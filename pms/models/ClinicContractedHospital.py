from django.db import models

from pms.models.BaseModel import BaseModel
from pms.models.Clinic import Clinic
from pms.models.Hospital import Hospital


class ClinicContractedHospital(BaseModel):
    clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE)
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE)