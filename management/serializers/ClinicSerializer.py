import traceback

from django.contrib.auth.models import User, Group
from django.db.transaction import atomic
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from management.serializers.GeneralSerializer import SelectSerializer, PageSerializer
from pms.models import Clinic, District, City, Staff, Profile, Branch


class ClinicSerializer(serializers.Serializer):
    clinicName = serializers.CharField()
    id = serializers.IntegerField(read_only=True)
    taxNumber = serializers.CharField()
    taxOffice = serializers.CharField()
    address = serializers.CharField()
    cityId = serializers.UUIDField(write_only=True)
    districtId = serializers.UUIDField(write_only=True)
    city = SelectSerializer(read_only=True)
    district = SelectSerializer(read_only=True)

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        try:
            clinic = Clinic()
            clinic.name = validated_data.get('clinicName')
            clinic.taxNumber = validated_data.get('taxNumber')
            clinic.taxOffice = validated_data.get('taxOffice')
            clinic.address = validated_data.get('address')
            clinic.district = District.objects.get(uuid=validated_data.get('districtId'))
            clinic.city = City.objects.get(uuid=validated_data.get('cityId'))
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


class ClinicStaffSerializer(serializers.Serializer):
    clinicId = serializers.UUIDField()
    firstName = serializers.CharField()
    lastName = serializers.CharField()
    email = serializers.CharField()
    groupId = serializers.IntegerField()
    diplomaNo = serializers.CharField()
    title = serializers.CharField()
    insuranceNo = serializers.CharField()
    branch = SelectSerializer()
    branchId = serializers.UUIDField()

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        try:
            with atomic:
                user = User()
                user.first_name = validated_data.get('firstName')
                user.last_name = validated_data.get('lastName')
                user.username = validated_data.get('email')
                user.email = validated_data.get('email')
                user.set_password('oxit2016')
                user.save()

                group = Group.objects.get(id=validated_data.get('groupId'))

                user.groups.add(group)
                user.save()

                profile = Profile()
                profile.user = user
                profile.save()

                staff = Staff()
                staff.title = validated_data.get('title')
                staff.profile = profile
                staff.branch = Branch.objects.get(uuid=validated_data.get('branchId'))
                staff.diplomaNo = validated_data.get('diplomaNo')
                staff.save()

                return staff
        except Exception as e:
            raise ValidationError("Lütfen tekrar deneyiniz")
