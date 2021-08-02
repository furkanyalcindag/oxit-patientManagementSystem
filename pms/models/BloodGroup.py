from django.db import models


class BloodGroup(models.Model):
    name = models.CharField(max_length=64)
