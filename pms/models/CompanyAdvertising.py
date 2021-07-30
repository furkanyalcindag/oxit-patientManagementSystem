from django.db import models

from pms.models import BaseModel
from pms.models.Advertising import Advertising
from pms.models.Company import Company


class CompanyAdvertising(BaseModel):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    ad = models.ForeignKey(Advertising, on_delete=models.CASCADE)
    publishStartDate = models.DateField()
    publishEndDate = models.DateField()
    price = models.IntegerField()
    name = models.CharField(max_length=256)
