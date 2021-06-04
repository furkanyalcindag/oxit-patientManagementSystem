from django.db import models

from pms.models import BaseModel, PaymentType


class PaymentMovement(BaseModel):
    paymentAmount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    creationDate = models.DateTimeField(auto_now_add=True, verbose_name='Kayıt Tarihi')
    modificationDate = models.DateTimeField(auto_now=True, verbose_name='Güncelleme Tarihi')
    paymentType = models.ForeignKey(PaymentType, on_delete=models.CASCADE, null=True, blank=True)
