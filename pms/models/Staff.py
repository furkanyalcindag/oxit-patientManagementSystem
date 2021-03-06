from django.db import models

from pms.models.Clinic import Clinic
from pms.models.Department import Department
from pms.models.BaseModel import BaseModel
from pms.models.Profile import Profile


class Staff(BaseModel):
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE)
    diplomaNo = models.CharField(max_length=256, null=True)
    insuranceNumber = models.CharField(max_length=256, null=True)
    title = models.CharField(max_length=256, null=False)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    profession = models.CharField(max_length=256)
    about = models.CharField(max_length=1028)
    clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE)
