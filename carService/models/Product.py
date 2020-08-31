import uuid as uuid
from django.db import models


class Product(models.Model):
    barcode_number = models.CharField(max_length=255)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    quantity = models.IntegerField()
    price =  models.DecimalField(max_digits=8, decimal_places=2)
