from django.db import models

from pms.models.Protocol import Protocol
from pms.models.BaseModel import BaseModel
from pms.models.PaymentSituation import PaymentSituation


class CheckingAccount(BaseModel):
    protocol = models.ForeignKey(Protocol, on_delete=models.CASCADE, null=True, blank=True)
    creationDate = models.DateTimeField(auto_now_add=True, verbose_name='Kayıt Tarihi')
    modificationDate = models.DateTimeField(auto_now=True, verbose_name='Güncelleme Tarihi')
    remainingDebt = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    paymentSituation = models.ForeignKey(PaymentSituation, on_delete=models.CASCADE, null=True, blank=True)
