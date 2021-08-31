# oxit staff serializer
import traceback

from django.contrib.auth.models import User, Group
from django.db import transaction
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework.exceptions import ValidationError

from management.serializers.GeneralSerializer import PageSerializer, SelectSerializer
from pms.models import Profile, Patient, Clinic
from pms.models.BloodGroup import BloodGroup
from pms.models.Gender import Gender


class PatientSerializer(serializers.Serializer):
    uuid = serializers.UUIDField(read_only=True)
    firstName = serializers.CharField()
    lastName = serializers.CharField()
    identityNumber = serializers.CharField()
    email = serializers.CharField()
    address = serializers.CharField()
    mobilePhone = serializers.CharField()
    genderId = serializers.IntegerField(write_only=True)
    gender = SelectSerializer(read_only=True)
    birthDate = serializers.DateField()
    bloodGroupId = serializers.IntegerField(write_only=True)
    bloodGroup = SelectSerializer(read_only=True)

    def update(self, instance, validated_data):
        try:
            with transaction.atomic():

                user = instance.profile.user
                user.first_name = validated_data.get('firstName')
                user.last_name = validated_data.get('lastName')
                user.email = validated_data.get('email')
                user.username = validated_data.get('email')
                user.save()
                instance.profile.mobilePhone = validated_data.get('mobilePhone')
                instance.profile.address = validated_data.get('address')
                instance.birthDate = validated_data.get('birthDate')
                instance.bloodGroup = BloodGroup.objects.get(id=validated_data.get('bloodGroupId'))
                instance.gender = Gender.objects.get(id=validated_data.get('genderId'))
                instance.save()

                return instance



        except Exception as e:
            traceback.print_exc()
            raise ValidationError("lütfen tekrar deneyiniz")

    def create(self, validated_data):
        try:
            with transaction.atomic():
                clinic = Clinic.objects.get(profile__user=self.context['request'].user)
                user = User.objects.create_user(username=validated_data.get('email'), email=validated_data.get('email'))
                user.first_name = validated_data.get('firstName')
                user.last_name = validated_data.get('lastName')
                user.set_password('oxit2016')
                group = Group.objects.get(name='Patient')
                user.groups.add(group)
                user.save()
                profile = Profile()
                profile.user = user
                profile.identityNumber = validated_data.get('identityNumber')
                profile.address = validated_data.get('address')
                profile.mobilePhone = validated_data.get('mobilePhone')
                profile.save()
                patient = Patient()
                patient.profile = profile
                patient.birthDate = validated_data.get('birthDate')
                patient.bloodGroup = BloodGroup.objects.get(id=validated_data.get('bloodGroupId'))
                patient.gender = Gender.objects.get(id=validated_data.get('genderId'))
                patient.clinic = clinic
                patient.save()
                return patient

        except Exception as e:
            traceback.print_exc()
            raise ValidationError("lütfen tekrar deneyiniz")

    def validate_email(self, email):

        user = None
        if self.instance is not None:

            user = Patient.objects.get(uuid=self.context['request'].query_params['id']).profile.user

            if User.objects.exclude(id=user.id).filter(username=email).count() > 0:
                raise serializers.ValidationError("Bu email sistemde kayıtlıdır")

        else:
            if User.objects.filter(username=email).count() > 0:
                raise serializers.ValidationError("Bu email sistemde kayıtlıdır")
        return email


class PatientPageableSerializer(PageSerializer):
    data = PatientSerializer(many=True)
    recordsTotal = serializers.IntegerField()
    recordsFiltered = serializers.IntegerField()
    activePage = serializers.IntegerField()

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass
