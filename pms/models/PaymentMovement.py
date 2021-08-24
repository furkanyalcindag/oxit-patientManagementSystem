from pms.models import PaymentType
from pms.models.CheckingAccount import CheckingAccount
from pms.models.BaseModel import BaseModel
from django.db import models


class PaymentMovement(BaseModel):
    paymentAmount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    checkingAccount = models.ForeignKey(CheckingAccount, on_delete=models.CASCADE)
    paymentType = models.ForeignKey(PaymentType, on_delete=models.CASCADE, null=True, blank=True)
