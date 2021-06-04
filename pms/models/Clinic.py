from django.db import models

from pms.models.BaseModel import BaseModel
from pms.models.City import City
from pms.models.District import District


class Clinic(BaseModel):
    name = models.CharField(max_length=256)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    address = models.CharField(max_length=256)
    about = models.TextField()
    telephoneNumber = models.CharField(max_length=256)
    logo = models.TextField()
    district = models.ForeignKey(District, on_delete=models.CASCADE)
    taxNumber = models.CharField(max_length=256)
    taxOffice = models.CharField(max_length=256)
