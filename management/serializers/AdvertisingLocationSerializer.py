import traceback
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from management.serializers.GeneralSerializer import PageSerializer, SelectSerializer
from pms.models.AdvertisingLocation import AdvertisingLocation


class AdvertisingLocationSerializer(serializers.Serializer):
    uuid = serializers.UUIDField(read_only=True)
    name = serializers.CharField()
    width = serializers.CharField()
    height = serializers.CharField()

    def update(self, instance, validated_data):
        try:
            instance.name = validated_data.get('name')
            instance.width = validated_data.get('width')
            instance.height = validated_data.get('height')
            instance.save()
            return instance
        except Exception as e:
            traceback.print_exc()
            raise ValidationError("lütfen tekrar deneyiniz")

    def create(self, validated_data):
        try:
            advertising = AdvertisingLocation()
            advertising.name = validated_data.get('name')
            advertising.width = validated_data.get('width')
            advertising.height = validated_data.get('height')
            advertising.save()
            return advertising

        except Exception as e:
            traceback.print_exc()
            raise ValidationError("lütfen tekrar deneyiniz")


class AdvertisingLocationPageableSerializer(PageSerializer):
    data = AdvertisingLocationSerializer(many=True)

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass
