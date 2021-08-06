from django.db import models

from pms.models import BaseModel
from pms.models.Protocol import Protocol


class Diagnosis(BaseModel):
    diagnosis = models.CharField(max_length=1028)
    protocol = models.ForeignKey(Protocol, on_delete=models.CASCADE)
