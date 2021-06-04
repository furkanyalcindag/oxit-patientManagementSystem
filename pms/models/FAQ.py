from django.db import models

from pms.models.BaseModel import BaseModel
from pms.models.Staff import Staff


class FAQ(BaseModel):
    question = models.TextField()
    answered = models.TextField()
    doctor = models.ForeignKey(Staff, on_delete=models.CASCADE)
