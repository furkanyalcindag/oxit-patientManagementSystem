# oxit staff serializer
import traceback

from django.contrib.auth.models import User, Group
from django.db import transaction
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from pms.models import CheckingAccount, PaymentSituation
from pms.models.ProtocolAssay import ProtocolAssay
from pmsDoctor.serializers.AssaySerializer import AssaySerializer
from pmsDoctor.serializers.GeneralSerializer import PageSerializer, SelectSerializer
from pms.models.Patient import Patient
from pms.models.Assay import Assay
from pms.models.Protocol import Protocol


class ProtocolSerializer(serializers.Serializer):
    uuid = serializers.UUIDField(read_only=True)
    patientId = serializers.CharField(write_only=True)
    patient = SelectSerializer(read_only=True)
    assays = serializers.ListSerializer(required=False, write_only=True, child=serializers.UUIDField())
    assayList = AssaySerializer(many=True, read_only=True, required=False)
    description = serializers.CharField()
    protocolId = serializers.IntegerField(read_only=True)
    price = serializers.DecimalField(max_digits=10, decimal_places=2)
    isPaid = serializers.BooleanField(default=False)
    taxRate = serializers.DecimalField(max_digits=10, decimal_places=2, write_only=True)

    # barcode = serializers.CharField()

    def update(self, instance, validated_data):
        try:
            with transaction.atomic():

                instance.patient = Patient.objects.get(uuid=validated_data.get('patientId'))
                for assayUUID in validated_data.get('assays'):
                    assay = Assay.objects.get(uuid=assayUUID)
                    instance.assay = assay
                    instance.save()
                instance.description = validated_data.get('description')
                if not instance.isPaid:
                    instance.price = 0
                else:
                    instance.price = validated_data.get('price')
                instance.save()
                return instance



        except Exception as e:
            traceback.print_exc()
            raise ValidationError("lütfen tekrar deneyiniz")

    def create(self, validated_data):
        try:
            with transaction.atomic():
                protocol = Protocol()

                protocol.patient = Patient.objects.get(uuid=validated_data.get('patientId'))
                protocol.description = validated_data.get('description')
                protocol.isPaid = validated_data.get('isPaid')
                if not protocol.isPaid:
                    protocol.price = 0
                    protocol.taxRate = 0
                else:
                    protocol.taxRate = validated_data.get('taxRate')
                    protocol.price = validated_data.get('price') + (
                            validated_data.get('price') * validated_data.get('taxRate') / 100)
                protocol.save()
                assayPrice = 0
                if validated_data.get('assays') is not None:
                    for assayUUID in validated_data.get('assays'):
                        assay = Assay.objects.get(uuid=assayUUID)
                        assayPrice += assay.price
                        protocolAssay = ProtocolAssay()
                        protocolAssay.assay = assay
                        protocolAssay.protocol = protocol
                        protocolAssay.save()
                totalPrice = assayPrice + protocol.price
                checking_account = CheckingAccount()
                checking_account.protocol = protocol
                checking_account.paymentSituation = PaymentSituation.objects.get(name__exact='Ödenmedi')
                checking_account.total = totalPrice
                checking_account.remainingDebt = totalPrice
                checking_account.save()
                protocol.save()
                return protocol

        except Exception as e:
            traceback.print_exc()
            raise ValidationError("lütfen tekrar deneyiniz")


class ProtocolPageableSerializer(PageSerializer):
    data = ProtocolSerializer(many=True)

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass
