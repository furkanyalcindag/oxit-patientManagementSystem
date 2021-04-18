from django.db import models

from career.models.BaseModel import BaseModel


class MilitaryStatus(BaseModel):
    keyword = models.CharField(max_length=64)
