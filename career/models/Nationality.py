from django.db import models


class Nationality(models.Model):
    name = models.CharField(max_length=128)
