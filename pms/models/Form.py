from django.db import models

from pms.models.BaseModel import BaseModel
from pms.models.Department import Department
from pms.models.Clinic import Clinic


class Form(BaseModel):
    name = models.CharField(max_length=128)
    clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE, null=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, null=True)
