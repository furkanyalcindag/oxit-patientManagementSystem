from django.db import models

from career.models.BaseModel import BaseModel
from career.models.Profile import Profile


class Student(BaseModel):
    studentNumber = models.CharField(max_length=64, null=False, blank=False)
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE)
    isGraduated = models.BooleanField(default=False)
    graduationDate = models.DateField(null=True, blank=True)
