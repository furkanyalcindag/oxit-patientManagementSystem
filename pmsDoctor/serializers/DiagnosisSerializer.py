# oxit staff serializer
import traceback
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from management.serializers.GeneralSerializer import PageSerializer, SelectSerializer
from pms.models import Protocol
from pms.models.Diagnosis import Diagnosis
from pms.models.Medicine import Medicine
from pms.models.MedicineDiagnosis import MedicineDiagnosis
from pms.models.ProtocolSituation import ProtocolSituation
from pmsDoctor.serializers.MedicineSerializer import MedicineSerializer


class DiagnosisSerializer(serializers.Serializer):
    uuid = serializers.UUIDField(read_only=True)
    diagnosis = serializers.CharField()
    protocolId = serializers.UUIDField(write_only=True)
    medicines = serializers.ListSerializer(required=False, write_only=True, child=serializers.CharField())
    medicineList = MedicineSerializer(many=True, read_only=True, required=False)

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        try:
            diagnosis = Diagnosis()
            protocol = Protocol.objects.get(uuid=validated_data.get('protocolId'))
            protocol.situation = ProtocolSituation.objects.get(name__exact='Sonuçlandı')
            protocol.save()
            diagnosis.diagnosis = validated_data.get('diagnosis')
            diagnosis.protocol = protocol
            diagnosis.save()
            if validated_data.get('medicines') is not None:
                for medicineName in validated_data.get('medicines'):
                    medicine = Medicine.objects.create(name=medicineName)
                    diagnosisMedicine = MedicineDiagnosis()
                    diagnosisMedicine.medicine = medicine
                    diagnosisMedicine.diagnosis = diagnosis
                    diagnosisMedicine.save()
            diagnosis.save()
            return diagnosis

        except Exception as e:
            traceback.print_exc()
            raise ValidationError("lütfen tekrar deneyiniz")


class DiagnosisPageableSerializer(PageSerializer):
    data = DiagnosisSerializer(many=True)

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass
