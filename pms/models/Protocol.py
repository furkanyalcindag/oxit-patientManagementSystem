from django.db import models

from pms.models import BaseModel
from pms.models.ProtocolType import ProtocolType
from pms.models.Patient import Patient
from pms.models.Hospital import Hospital

class Protocol(BaseModel):

    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, null=True, blank=True)
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE, null=True, blank=True)
    description = models.CharField(max_length=500, blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.DecimalField(max_digits=10, decimal_places=2)
    totalPrice = models.DecimalField(max_digits=10, decimal_places=2)
    isOrder = models.BooleanField(default=False)
    creationDate = models.DateTimeField(auto_now_add=True, verbose_name='Kayıt Tarihi')
    modificationDate = models.DateTimeField(auto_now=True, verbose_name='Güncelleme Tarihi')
    protocolType = models.ForeignKey(ProtocolType, on_delete=models.CASCADE, null=True, blank=True)
    doctorComment = models.TextField()
    patientComment = models.TextField()
    report = models.TextField()
    isDeleted = models.BooleanField(default=False)

