import traceback
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from management.serializers.GeneralSerializer import PageSerializer, SelectSerializer
from pms.models.CompanyAdvertising import CompanyAdvertising
from pms.models.Company import Company
from pms.models.Advertising import Advertising


class CompanyAdvertisingSerializer(serializers.Serializer):
    uuid = serializers.UUIDField(read_only=True)
    name = serializers.CharField()
    companyId = serializers.IntegerField(write_only=True)
    locationId = serializers.IntegerField(write_only=True)
    company = SelectSerializer(read_only=True)
    location = SelectSerializer(read_only=True)
    publishStartDate = serializers.DateField()
    publishEndDate = serializers.DateField()
    price = serializers.IntegerField()

    def update(self, instance, validated_data):
        try:
            instance.name = validated_data.get('name')
            instance.company = Company.objects.get(id=validated_data.get('companyId'))
            instance.ad = Advertising.objects.get(id=validated_data.get('locationId'))
            instance.publishStartDate = validated_data.get('publishStartDate')
            instance.publishEndDate = validated_data.get('publishEndDate')
            instance.price = validated_data.get('price')
            instance.save()
            return instance
        except:
            traceback.print_exc()
            raise ValidationError("lütfen tekrar deneyiniz")

    def create(self, validated_data):
        try:
            advertising = CompanyAdvertising()
            advertising.name = validated_data.get('name')
            advertising.company = Company.objects.get(id=validated_data.get('companyId'))
            advertising.ad = Advertising.objects.get(id=validated_data.get('locationId'))
            advertising.publishStartDate = validated_data.get('publishStartDate')
            advertising.publishEndDate = validated_data.get('publishEndDate')
            advertising.price = validated_data.get('price')
            advertising.save()
            return advertising

        except Exception as e:
            traceback.print_exc()
            raise ValidationError("lütfen tekrar deneyiniz")


class CompanyAdvertisingPageableSerializer(PageSerializer):
    data = CompanyAdvertisingSerializer(many=True)

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass
