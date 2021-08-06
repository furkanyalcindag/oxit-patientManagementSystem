from django.db import models



class Medicine(models.Model):
    name = models.CharField(max_length=1028)
