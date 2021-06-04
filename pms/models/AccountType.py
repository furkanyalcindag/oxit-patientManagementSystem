from django.db import models

from pms.models.BaseModel import BaseModel


class AccountType(BaseModel):
    name = models.CharField(max_length=128)
