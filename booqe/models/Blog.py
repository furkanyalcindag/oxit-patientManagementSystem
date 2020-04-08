from django.db import models

from booqe.models.Profile import Profile
from booqe.models.Category import Category



class Blog(models.Model):
    blogOwner = models.ForeignKey(Profile, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    blog = models.TextField(blank=True)
    description = models.TextField(blank=True,null=True)
    tags = models.CharField(max_length=1000)
    isPublish = models.BooleanField()
    creationDate = models.DateTimeField(auto_now_add=True, verbose_name='Kayıt Tarihi')
    modificationDate = models.DateTimeField(auto_now=True, verbose_name='Güncelleme Tarihi')
    categories = models.ManyToManyField(Category, verbose_name='Kategori')
