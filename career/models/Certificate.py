import uuid as uuid
from django.db import models

from career.models.BaseModel import BaseModel
from career.models.Student import Student


class Certificate(BaseModel):
    name = models.CharField(max_length=256, null=False)
    institutionName = models.CharField(max_length=256, null=True)
    certificateNo = models.CharField(max_length=256, null=True)
    description = models.TextField(null=True)
    year = models.IntegerField(null=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)