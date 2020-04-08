from django.db import models


class Category(models.Model):
    categoryName = models.CharField(max_length=200)

    def __str__(self):
        return '%s ' % self.categoryName