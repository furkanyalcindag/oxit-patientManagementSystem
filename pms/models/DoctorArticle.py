from django.db import models

from pms.models.BaseModel import BaseModel
from pms.models.Staff import Staff


class DoctorArticle(BaseModel):
    title = models.CharField(max_length=128)
    link = models.CharField(max_length=256)
    doctor = models.ForeignKey(Staff, on_delete=models.CASCADE)
    date = models.DateField()
