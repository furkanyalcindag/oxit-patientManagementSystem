from django.db import models

from pms.models.Clinic import Clinic
from pms.models.BaseModel import BaseModel


class ClinicMedia(BaseModel):
    clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE)
    media = models.TextField()
