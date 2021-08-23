from pms.models.PaymentSituation import PaymentSituation
from pms.models.Protocol import Protocol
from pms.models.BaseModel import BaseModel
from django.db import models


class CheckingAccount(BaseModel):
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)  # toplam
    protocol = models.ForeignKey(Protocol, on_delete=models.CASCADE)
    remainingDebt = models.DecimalField(max_digits=10, decimal_places=2, default=0)  # kalan
    paymentSituation = models.ForeignKey(PaymentSituation, on_delete=models.CASCADE, null=True, blank=True)