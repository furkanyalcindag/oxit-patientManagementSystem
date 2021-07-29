from django.db import models

from pms.models import BaseModel
from pms.models.AdvertisingLocation import AdvertisingLocation
from pms.models.Company import Company


class Advertising(BaseModel):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    ad = models.ForeignKey(AdvertisingLocation, on_delete=models.CASCADE)
    publishStartDate = models.DateField()
    publishEndDate = models.DateField()
    price = models.IntegerField()
    name = models.CharField(max_length=256)
