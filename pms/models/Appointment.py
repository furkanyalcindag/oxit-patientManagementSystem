from django.db import models

from pms.models.Patient import Patient
from pms.models.BaseModel import BaseModel
from pms.models.Staff import Staff


class Appointment(BaseModel):
    doctor = models.ForeignKey(Staff, on_delete=models.CASCADE)
    time = models.TimeField()
    date = models.DateField()
    isCome = models.BooleanField(default=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    endTime = models.TimeField()
