from django.db import models
from pms.models.BaseModel import BaseModel
from pms.models.Staff import Staff


class Media(BaseModel):
    doctor = models.ForeignKey(Staff, on_delete=models.CASCADE)
    media = models.TextField()
