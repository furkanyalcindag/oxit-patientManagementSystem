from django.db import models

from career.models.JobPost import JobPost
from career.models.BaseModel import BaseModel
from career.models.Department import Department


class JobPostDepartment(BaseModel):
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    jobPost = models.ForeignKey(JobPost, on_delete=models.CASCADE)
