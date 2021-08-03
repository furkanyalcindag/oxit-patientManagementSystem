import traceback

from django.db import transaction
from rest_framework import serializers
from django.contrib.auth.models import User, Group
from rest_framework.exceptions import ValidationError

from pms.models import Staff, Department, Profile
from pmsDoctor.serializers.GeneralSerializer import SelectSerializer, PageSerializer


class DoctorSerializer(serializers.Serializer):
    uuid = serializers.UUIDField(read_only=True)
    firstName = serializers.CharField()
    lastName = serializers.CharField()
    diplomaNo = serializers.CharField()
    insuranceNumber = serializers.CharField()
    title = serializers.CharField()
    departmentId = serializers.IntegerField(write_only=True)
    department = SelectSerializer(read_only=True)
    email = serializers.CharField()

    def update(self, instance, validated_data):
        user = instance.profile.user
        user.first_name = validated_data.get('firstName')
        user.last_name = validated_data.get('lastName')
        user.email = validated_data.get('email')
        user.username = validated_data.get('email')
        user.save()
        instance.diplomaNo = validated_data.get('diplomaNo')
        instance.insuranceNumber = validated_data.get('insuranceNumber')
        instance.title = validated_data.get('title')
        instance.department = Department.objects.get(id=validated_data.get('departmentId'))
        instance.save()

        return instance

    def create(self, validated_data):
        try:
            with transaction.atomic():
                user = User.objects.create_user(username=validated_data.get('email'),
                                                email=validated_data.get('email'))
                user.first_name = validated_data.get('firstName')
                user.last_name = validated_data.get('lastName')
                user.set_password('oxit2016')
                group = Group.objects.get(name='Doctor')
                user.groups.add(group)
                user.save()
                profile = Profile()
                profile.user = user
                profile.save()
                staff = Staff()
                staff.profile = profile
                staff.diplomaNo = validated_data.get('diplomaNo')
                staff.insuranceNumber = validated_data.get('insuranceNumber')
                staff.title = validated_data.get('title')
                staff.department = Department.objects.get(id=int(validated_data.get('departmentId')))
                staff.save()

                return staff
        except:
            traceback.print_exc()
            raise ValidationError("lütfen tekrar deneyiniz")

    def validate_email(self, email):

        user = None
        if self.instance is not None:

            user = Staff.objects.get(uuid=self.context['request'].query_params['id']).profile.user

            if User.objects.exclude(id=user.id).filter(username=email).count() > 0:
                raise serializers.ValidationError("Bu email sistemde kayıtlıdır")

        else:
            if User.objects.filter(username=email).count() > 0:
                raise serializers.ValidationError("Bu email sistemde kayıtlıdır")
        return email


class DoctorPageSerializer(PageSerializer):
    data = DoctorSerializer(many=True)

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass
