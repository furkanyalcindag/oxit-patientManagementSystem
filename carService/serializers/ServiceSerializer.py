from rest_framework import serializers

from carService.models.Car import Car
from carService.models.Service import Service
from carService.models.Situation import Situation
from carService.models.ServiceType import ServiceType


class SituationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Situation
        fields = '__all__'


class ServiceTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceType
        fields = '__all__'


class ServiceSerializer(serializers.Serializer):
    carUUID = serializers.UUIDField()
    serviceType = serializers.IntegerField()
    serviceKM = serializers.IntegerField()
    complaint = serializers.CharField()
    serviceSituation = serializers.CharField(read_only=True)

    def create(self, validated_data):
        try:
            service = Service()
            service.complaint = validated_data.get('complaint')
            service.car = Car.objects.get(uuid=validated_data.get('carUUID'))
            service.serviceType = ServiceType.objects.get(id=validated_data.get('serviceType'))
            service.save()

        except:
            raise serializers.ValidationError("lütfen tekrar deneyiniz")
