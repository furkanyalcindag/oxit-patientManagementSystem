import uuid as uuid
from django.db import models

from career.models.BaseModel import BaseModel
from career.models.JobType import JobType
from career.models.Student import Student


class JobInfo(BaseModel):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    company = models.CharField(max_length=256, blank=True, null=True)
    title = models.CharField(max_length=256)
    startDate = models.DateField()
    isContinue = models.BooleanField(default=True)
    finishDate = models.DateField()
    description = models.TextField(null=True, blank=True)
    jobType = models.ForeignKey(JobType, on_delete=models.CASCADE)
