from django.db import models

from carService.models.Product import Product
from carService.models.Service import Service


class ServiceProduct(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE, null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True)
    productTotalPrice = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    quantity = models.IntegerField(default=1)
