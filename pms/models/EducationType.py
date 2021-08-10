from django.db import models



class EducationType(models.Model):
    name = models.CharField(max_length=64, null=True, blank=True)
