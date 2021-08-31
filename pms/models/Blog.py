from django.db import models

from pms.models.Department import Department
from pms.models.BaseModel import BaseModel
from pms.models.Profile import Profile


class Blog(BaseModel):
    keyword = models.TextField(max_length=1028, default=True, blank=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Profile, on_delete=models.CASCADE)
    image = models.TextField(null=True, blank=True)
    isPublish = models.BooleanField(default=False)
    description = models.TextField()
    title = models.CharField(max_length=1028)
    isSponsored = models.BooleanField(default=False)