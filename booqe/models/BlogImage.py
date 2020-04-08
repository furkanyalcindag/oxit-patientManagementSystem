from django.db import models

from booqe.models.Blog import Blog


class BlogImage(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, default=None)
    blogImage = models.ImageField(upload_to='blog-images/', null=True, blank=True, verbose_name='Blog Resim')
