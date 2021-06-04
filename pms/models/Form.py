from django.db import models

from pms.models.BaseModel import BaseModel
from pms.models.Branch import Branch
from pms.models.Clinic import Clinic


class Form(BaseModel):
    name = models.CharField(max_length=128)
    clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE, null=True)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, null=True)
