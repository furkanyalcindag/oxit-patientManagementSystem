from django.db import models

from pms.models.BaseModel import BaseModel
from pms.models.Form import Form
from pms.models.FormParameter import FormParameter


class FormFormParameter(BaseModel):
    form = models.ForeignKey(Form, on_delete=models.CASCADE)
    formParameter = models.ForeignKey(FormParameter, on_delete=models.CASCADE)
