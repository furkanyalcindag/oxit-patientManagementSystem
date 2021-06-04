from django.db import models

from pms.models.BaseModel import BaseModel
from pms.models.Profile import Profile


class Patient(BaseModel):
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE)

