import uuid as uuid
from django.db import models


class Product(models.Model):
    barcodeNumber = models.CharField(max_length=255)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255,null=True)
    quantity = models.IntegerField(default=0)
    netPrice = models.DecimalField(max_digits=8, decimal_places=2,default=0)
    productImage = models.ImageField(upload_to='product/', null=True, blank=True, verbose_name='Ürün Resmi')
    isOpen = models.BooleanField(null=True, default=True)
    taxRate = models.DecimalField(max_digits=8, decimal_places=2,default=0)
    totalProduct =  models.DecimalField(max_digits=8, decimal_places=2,default=0)


