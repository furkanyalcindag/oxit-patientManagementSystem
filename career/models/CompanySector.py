import uuid as uuid
from django.db import models

from career.models.BaseModel import BaseModel
from career.models.Company import Company
from career.models.Sector import Sector


class CompanySector(BaseModel):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    sector = models.ForeignKey(Sector, on_delete=models.CASCADE)
