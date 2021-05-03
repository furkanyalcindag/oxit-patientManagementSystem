from django.db import models

from career.models.Blog import Blog
from career.models.BaseModel import BaseModel
from career.models.Language import Language


class BlogDescription(BaseModel):
    title = models.CharField(max_length=256)
    article = models.TextField()
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    language = models.ForeignKey(Language, on_delete=models.CASCADE)
