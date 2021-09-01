from django.db import models

from pms.models.Patient import Patient
from pms.models.Clinic import Clinic


class PatientClinic(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE)
