from django.db import models

from career.models.BaseModel import BaseModel
from career.models.Profile import Profile


class Instructor(BaseModel):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
