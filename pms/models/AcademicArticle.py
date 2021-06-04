from django.db import models

from pms.models.BaseModel import BaseModel
from pms.models.Category import Category
from pms.models.Profile import Profile


class AcademicArticle(BaseModel):
    keyword = models.CharField(max_length=128, default=True, blank=True)
    title = models.CharField(max_length=128)
    date = models.DateField()
    article = models.TextField()
    doctor = models.ForeignKey(Profile, on_delete=models.CASCADE)

