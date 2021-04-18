from django.db import models

from career.models.BaseModel import BaseModel
from career.models.Profile import Profile
from career.models.Sector import Sector


class Consultant(BaseModel):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    sector = models.ForeignKey(Sector, on_delete=models.CASCADE)
    speciality = models.CharField(max_length=128, null=True, blank=True)
    isPaid = models.BooleanField(default=False)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
