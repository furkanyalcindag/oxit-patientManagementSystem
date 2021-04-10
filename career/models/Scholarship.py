import uuid as uuid
from django.db import models

from career.models.BaseModel import BaseModel
from career.models.Company import Company


class Scholarship(BaseModel):
    name = models.CharField(max_length=256, null=True)
    description = models.TextField(null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
