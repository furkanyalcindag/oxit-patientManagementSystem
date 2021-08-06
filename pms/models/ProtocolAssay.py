from django.db import models

from pms.models.Assay import Assay
from pms.models.BaseModel import BaseModel
from pms.models.Protocol import Protocol


class ProtocolAssay(BaseModel):
    protocol = models.ForeignKey(Protocol, on_delete=models.CASCADE)
    assay = models.ForeignKey(Assay, on_delete=models.CASCADE)
