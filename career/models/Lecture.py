from django.db import models

from career.models.BaseModel import BaseModel
from career.models.Instructor import Instructor


class Lecture(BaseModel):
    name = models.CharField(max_length=128)
    capacity = models.IntegerField()
    date = models.DateField()
    time = models.TimeField()
    place = models.CharField(max_length=128)
    isPaid = models.BooleanField(default=False)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    instructor = models.ForeignKey(Instructor, on_delete=models.CASCADE)
