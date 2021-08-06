from django.db import models

from pms.models.Diagnosis import Diagnosis
from pms.models.Medicine import Medicine


class MedicineDiagnosis(models.Model):
    diagnosis = models.ForeignKey(Diagnosis, on_delete=models.CASCADE)
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE)
