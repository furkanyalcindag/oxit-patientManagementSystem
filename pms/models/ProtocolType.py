from django.db import models

from pms.models import BaseModel


class ProtocolType(BaseModel):
    name = models.CharField(max_length=255, blank=True, null=True)