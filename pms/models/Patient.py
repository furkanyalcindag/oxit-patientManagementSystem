from django.db import models

from pms.models.BaseModel import BaseModel
from pms.models.BloodGroup import BloodGroup
from pms.models.Gender import Gender
from pms.models.Profile import Profile


class Patient(BaseModel):
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE)
    birthDate = models.DateField()
    gender = models.ForeignKey(Gender, on_delete=models.CASCADE)
    bloodGroup = models.ForeignKey(BloodGroup, on_delete=models.CASCADE)
    debtPaidOff = models.DecimalField(max_digits=10, decimal_places=2, default=0)
