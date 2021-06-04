from django.db import models

from pms.models.AccountType import AccountType
from pms.models.BaseModel import BaseModel
from pms.models.Clinic import Clinic


class Account(BaseModel):
    name = models.CharField(max_length=128)
    type = models.ForeignKey(AccountType, on_delete=models.CASCADE)
    clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE)
