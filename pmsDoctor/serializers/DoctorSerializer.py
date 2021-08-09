import traceback

from django.contrib.auth.models import User, Group
from django.db import transaction
from rest_framework import serializers
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


class DoctorGeneralInfoSerializer(serializers.Serializer):
    uuid = serializers.UUIDField(read_only=True)
    firstName = serializers.CharField(read_only=True)
    lastName = serializers.CharField(read_only=True)
    profileImage = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    diplomaNo = serializers.CharField()
    department = SelectSerializer(read_only=True)
    departmentId = serializers.IntegerField(write_only=True)
    profession = serializers.CharField(required=False, allow_blank=True)
    title = serializers.CharField(required=False, allow_blank=True)

    def update(self, instance, validated_data):
        try:
            instance.profileImage = validated_data.get('profileImage')
            instance.department = Department.objects.get(id=validated_data.get('departmentId'))
            instance.profession = validated_data.get('profession')
            instance.title = validated_data.get('title')
            instance.save()
            return instance
        except:
            traceback.print_exc()
            raise serializers.ValidationError("lütfen tekrar deneyiniz")

    def create(self, validated_data):
        pass


class DoctorAboutSerializer(serializers.Serializer):
    uuid = serializers.UUIDField(read_only=True)
    about = serializers.CharField(required=False, allow_blank=True)

    def update(self, instance, validated_data):
        try:
            instance.about = validated_data.get('about')
            instance.save()
            return instance
        except:
            traceback.print_exc()
            raise serializers.ValidationError("lütfen tekrar deneyiniz")

    def create(self, validated_data):
        pass


class DoctorContactInfoSerializer(serializers.Serializer):
    uuid = serializers.UUIDField(read_only=True)
    email = serializers.CharField(read_only=True)
    address = serializers.CharField(required=False, allow_blank=True)
    website = serializers.CharField(required=False, allow_blank=True)
    youtube = serializers.CharField(required=False, allow_blank=True)
    facebook = serializers.CharField(required=False, allow_blank=True)
    linkedin = serializers.CharField(required=False, allow_blank=True)
    instagram = serializers.CharField(required=False, allow_blank=True)
    mobilePhone = serializers.CharField(required=False, allow_blank=True)

    def update(self, instance, validated_data):
        try:
            user = instance.user
            user.save()
            instance.address = validated_data.get('address')
            instance.website = validated_data.get('website')
            instance.youtube = validated_data.get('youtube')
            instance.facebook = validated_data.get('facebook')
            instance.linkedin = validated_data.get('linkedin')
            instance.instagram = validated_data.get('instagram')
            instance.mobilePhone = validated_data.get('mobilePhone')
            instance.save()
            return instance
        except:
            traceback.print_exc()
            raise serializers.ValidationError("lütfen tekrar deneyiniz")

    def create(self, validated_data):
        pass
