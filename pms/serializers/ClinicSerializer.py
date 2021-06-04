import traceback

from django.contrib.auth.models import User
from django.db import transaction
from rest_framework import serializers
from django.contrib.auth.models import User, Group
from rest_framework.validators import UniqueValidator

from oxiterp.serializers import UserSerializer
from pms.models import Clinic, Profile
from pms.serializers.GeneralSerializers import PageSerializer


class ClinicSerializer(serializers.Serializer):
    # TODO: Clinic serializer

    name = serializers.CharField(required=False)
    taxNumber = serializers.CharField(required=False)
    taxOffice = serializers.CharField(read_only=False)

    def create(self, validated_data):
        try:

            clinic = Clinic()
            clinic.name = validated_data.get('name')
            clinic.taxNumber = validated_data.get('taxNumber')
            clinic.taxOffice = validated_data.get('taxOffice')
            clinic.save()




            return clinic
        except Exception:
            traceback.print_exc()
            raise serializers.ValidationError("lütfen tekrar deneyiniz")


class ClinicPageableSerializer(PageSerializer):
    data = ClinicSerializer(many=True)

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass