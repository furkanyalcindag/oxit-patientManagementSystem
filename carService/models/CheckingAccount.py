from django.db import models

from carService.models.PaymentSituation import PaymentSituation
from carService.models.Service import Service


class CheckingAccount(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE, null=True, blank=True)
    creationDate = models.DateTimeField(auto_now_add=True, verbose_name='Kayıt Tarihi')
    modificationDate = models.DateTimeField(auto_now=True, verbose_name='Güncelleme Tarihi')
    remainingDebt = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    paymentSituation = models.ForeignKey(PaymentSituation, on_delete=models.CASCADE, null=True, blank=True)
