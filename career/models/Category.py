from django.db import models


class Category(models.Model):
    keyword = models.CharField(max_length=256)
