from django.db import models

from pms.models.BaseModel import BaseModel
from pms.models.Branch import Branch
from pms.models.Profile import Profile


class Staff(BaseModel):
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE)
    diplomaNo = models.CharField(max_length=256, null=True)
    insuranceNumber = models.CharField(max_length=256, null=True)
    title = models.CharField(max_length=256, null=False)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)