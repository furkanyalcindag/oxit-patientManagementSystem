from django.db import models

from pms.models.BaseModel import BaseModel
from pms.models.City import City
from pms.models.District import District


class Clinic(BaseModel):
    name = models.CharField(max_length=256)
    city = models.ForeignKey(City, on_delete=models.CASCADE,null=True)
    address = models.CharField(max_length=256)
    about = models.TextField()
    telephoneNumber = models.CharField(max_length=256)
    logo = models.TextField()
    district = models.ForeignKey(District, on_delete=models.CASCADE,null=True)
    website = models.CharField(max_length=128, null=True, blank=True)
    taxNumber = models.CharField(max_length=256)
    taxOffice = models.CharField(max_length=256)
    staffCount = models.IntegerField(default=0)
    fax = models.CharField(max_length=20, null=True, blank=True)
    locationMap = models.TextField()