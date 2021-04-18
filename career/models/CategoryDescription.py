from django.db import models

from career.models.BaseModel import BaseModel
from career.models.Category import Category
from career.models.Language import Language


class CategoryDescription(BaseModel):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=256)
    language = models.ForeignKey(Language, on_delete=models.CASCADE)

