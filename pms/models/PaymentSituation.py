from django.db import models

from pms.models import BaseModel


class PaymentSituation(BaseModel):
    name = models.CharField(max_length=255, null=True, blank=True)