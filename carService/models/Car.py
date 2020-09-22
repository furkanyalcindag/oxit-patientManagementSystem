from django.db import models

from carService.models.Profile import Profile


class Car(models.Model):

    plate = models.CharField(max_length=200, blank=True, null=True)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, default=None)
    brand = models.CharField(max_length=200, blank=True, null=True)
    model = models.CharField(max_length=200, blank=True, null=True)
    year = models.IntegerField(blank=True, null=True)
    engine = models.CharField(max_length=200, blank=True, null=True)
    oilType = models.CharField(max_length=200, blank=True, null=True)
