# oxit staff serializer
import traceback

from django.contrib.auth.models import User, Group
from django.db import transaction
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from pmsDoctor.serializers.AssaySerializer import AssaySerializer
from pmsDoctor.serializers.GeneralSerializer import PageSerializer, SelectSerializer
from pms.models.Patient import Patient
from pms.models.Assay import Assay
from pms.models.Protocol import Protocol


class ProtocolSerializer(serializers.Serializer):
    uuid = serializers.UUIDField(read_only=True)
    patientId = serializers.CharField(write_only=True)
    patient = SelectSerializer(read_only=True)
    assays = serializers.ListSerializer(write_only=True, child=serializers.UUIDField())
    assayList = AssaySerializer(many=True, read_only=True, required=False)
    description = serializers.CharField()

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
                for assayUUID in validated_data.get('assays'):
                    assay = Assay.objects.get(uuid=assayUUID)
                    protocol.assay = assay
                    protocol.save()
                protocol.description = validated_data.get('description')
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
