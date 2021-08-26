from django.db import models

from pms.models.BaseModel import BaseModel


class Assay(BaseModel):
    name = models.CharField(max_length=256)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    taxRate = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    isPrice = models.BooleanField(default=False)
