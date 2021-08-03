import traceback

from django.contrib.auth.models import User, Group
from django.db import transaction
from django.db.transaction import atomic
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.validators import UniqueValidator

from management.serializers.GeneralSerializer import SelectSerializer, PageSerializer
from pms.models import Clinic, District, City, Staff, Profile


class ClinicSerializer(serializers.Serializer):
    clinicName = serializers.CharField()
    uuid = serializers.UUIDField(read_only=True)
    taxNumber = serializers.CharField()
    taxOffice = serializers.CharField()
    address = serializers.CharField()
    cityId = serializers.IntegerField(write_only=True)
    districtId = serializers.IntegerField(write_only=True)
    city = SelectSerializer(read_only=True)
    district = SelectSerializer(read_only=True)
    cityDistrict = serializers.CharField(allow_blank=False, read_only=True, allow_null=True)
    email = serializers.CharField(required=True, validators=[UniqueValidator(queryset=User.objects.all())])
    staffName = serializers.CharField(required=True, allow_null=True, allow_blank=True)
    staffSurname = serializers.CharField(required=True, allow_null=True, allow_blank=True)
    telephoneNumber = serializers.CharField(required=True, allow_null=True, allow_blank=True)

    def update(self, instance, validated_data):
        try:
            instance.name = validated_data.get('clinicName')
            instance.taxNumber = validated_data.get('taxNumber')
            instance.taxOffice = validated_data.get('taxOffice')
            instance.address = validated_data.get('address')
            instance.district = District.objects.get(id=validated_data.get('districtId'))
            instance.city = City.objects.get(id=validated_data.get('cityId'))
            instance.save()

            return instance

        except Exception as e:
            traceback.print_exc()
            raise ValidationError("lütfen tekrar deneyiniz")

    def create(self, validated_data):
        try:
            with transaction.atomic():
                user = User.objects.create_user(username=validated_data.get('email'), email=validated_data.get('email'))
                user.first_name = validated_data.get('staffName')
                user.last_name = validated_data.get('staffSurname')
                user.set_password('oxit2016')
                group = Group.objects.get(name='Clinic')
                user.groups.add(group)
                user.save()
                profile = Profile.objects.create(user=user)
                profile.save()
                clinic = Clinic(profile=profile)
                clinic.name = validated_data.get('clinicName')
                clinic.taxNumber = validated_data.get('taxNumber')
                clinic.taxOffice = validated_data.get('taxOffice')
                clinic.address = validated_data.get('address')
                clinic.telephoneNumber = validated_data.get('telephoneNumber')
                clinic.district = District.objects.get(id=validated_data.get('districtId'))
                clinic.city = City.objects.get(id=validated_data.get('cityId'))
                clinic.save()

                return clinic

        except Exception as e:
            traceback.print_exc()
            raise ValidationError("lütfen tekrar deneyiniz")


class ClinicPageableSerializer(PageSerializer):
    data = ClinicSerializer(many=True)

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass
