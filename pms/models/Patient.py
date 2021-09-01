from django.db import models

from pms.models.Clinic import Clinic
from pms.models.BaseModel import BaseModel
from pms.models.BloodGroup import BloodGroup
from pms.models.Gender import Gender
from pms.models.Profile import Profile


class Patient(BaseModel):
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE)
    birthDate = models.DateField(null=True, blank=True)
    gender = models.ForeignKey(Gender, on_delete=models.CASCADE, null=True, blank=True)
    bloodGroup = models.ForeignKey(BloodGroup, on_delete=models.CASCADE, null=True, blank=True)
    debtPaidOff = models.DecimalField(max_digits=10, decimal_places=2, default=0)