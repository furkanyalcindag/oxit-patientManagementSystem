from django.db import models

from pms.models.BaseModel import BaseModel
from pms.models.Category import Category
from pms.models.Profile import Profile


class Blog(BaseModel):
    keyword = models.CharField(max_length=128, default=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Profile, on_delete=models.CASCADE)
