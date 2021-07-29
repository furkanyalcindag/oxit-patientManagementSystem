
from django.db import models
from pms.models import BaseModel



class Notification(BaseModel):

    body = models.CharField(max_length=128)
    link = models.CharField(max_length=128,null=True)
    title = models.CharField(max_length=128)
    image = models.TextField(null=True, blank=True)
