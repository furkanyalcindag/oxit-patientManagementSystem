from django.db import models

from booqe.models import Category


class CategoryImage(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=None)
    categoryImage = models.ImageField(upload_to='category-images/', null=True, blank=True, verbose_name='Category Resim')
