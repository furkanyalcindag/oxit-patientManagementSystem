from django.db import models

from pms.models.BaseModel import BaseModel
from pms.models.Clinic import Clinic
from pms.models.Staff import Staff


class ClinicStaff(BaseModel):
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE)
    clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE)
