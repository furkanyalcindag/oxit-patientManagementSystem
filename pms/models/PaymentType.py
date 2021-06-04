from django.db import models

from pms.models.BaseModel import BaseModel


class PaymentType(BaseModel):
    name = models.CharField(max_length=128)
