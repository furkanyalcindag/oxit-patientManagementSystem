import uuid as uuid
from django.db import models

from carService.models.Car import Car


class Service(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    car = models.ForeignKey(Car, on_delete=models.CASCADE, null=True, blank=True)
    description = models.CharField(max_length=500, blank=True, null=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    discount = models.DecimalField(max_digits=8, decimal_places=2)
    total_price = models.DecimalField(max_digits=8, decimal_places=2)
    is_order = models.BooleanField()
