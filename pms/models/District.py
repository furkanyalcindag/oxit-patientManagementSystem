from django.db import models

from pms.models.BaseModel import BaseModel
from pms.models.City import City


class District(BaseModel):
    name = models.CharField(max_length=64)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
