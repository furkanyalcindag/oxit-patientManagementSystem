from django.db import models

from career.models.BaseModel import BaseModel
from career.models.Profile import Profile


class Company(BaseModel):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    city = models.CharField(max_length=255, blank=True, null=True)
    district = models.CharField(max_length=100, blank=True, null=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    taxNumber = models.CharField(max_length=128, null=True, blank=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    logo = models.TextField(null=True, blank=True)
    taxOffice = models.CharField(max_length=255, null=True, blank=True)
    staffCount = models.IntegerField(default=0)
    about = models.TextField(null=True, blank=True)
    year = models.IntegerField(default=0)
    isInstitution = models.BooleanField(default=False)
    website = models.CharField(max_length=128, null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    fax = models.CharField(max_length=20, null=True, blank=True)
    locationMap = models.TextField()
