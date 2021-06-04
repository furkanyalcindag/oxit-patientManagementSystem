from django.db import models

from pms.models.BaseModel import BaseModel
from pms.models.Staff import Staff


class DoctorVideo(BaseModel):
    doctor = models.ForeignKey(Staff, on_delete=models.CASCADE)
    videoLink = models.CharField(max_length=256)
