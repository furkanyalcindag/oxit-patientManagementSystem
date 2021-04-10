from django.db import models

from career.models.BaseModel import BaseModel
from career.models.Language import Language


class BlogDescription(BaseModel):
    title = models.CharField(max_length=256)
    article = models.TextField()
    language = models.ForeignKey(Language, on_delete=models.CASCADE)
    isDeleted = models.BooleanField(default=False)
