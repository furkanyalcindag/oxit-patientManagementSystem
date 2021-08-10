from django.db import models

from pms.models import BaseModel
from pms.models.EducationType import EducationType


class DoctorEducation(BaseModel):
    educationType = models.ForeignKey(EducationType, on_delete=models.CASCADE)
    universityName = models.CharField(max_length=256)
    facultyName = models.CharField(max_length=256)
    departmentName = models.CharField(max_length=256)

