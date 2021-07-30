from django.db import models
from django.contrib.auth.models import User

from pms.models.BaseModel import BaseModel


class Company(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=256)
    taxOffice = models.CharField(max_length=256)
    taxNumber = models.CharField(max_length=256)
