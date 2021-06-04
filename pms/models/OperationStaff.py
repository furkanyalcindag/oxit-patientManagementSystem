from django.db import models

from pms.models.BaseModel import BaseModel
from pms.models.Operation import Operation
from pms.models.Staff import Staff


class OperationStaff(BaseModel):
    operation = models.ForeignKey(Operation, on_delete=models.CASCADE)
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE)

