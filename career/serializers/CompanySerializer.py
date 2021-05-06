import traceback

from django.contrib.auth.models import User, Group
from django.db import transaction
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from career.models import Profile, Company
from career.serializers.GeneralSerializers import PageSerializer
from oxiterp.serializers import UserSerializer


class CompanySerializer(serializers.Serializer):
    # TODO: Company serializer
    uuid = serializers.UUIDField(read_only=True)
    user = UserSerializer(read_only=True)
    firstName = serializers.CharField(required=True)
    lastName = serializers.CharField(required=True)
    email = serializers.CharField(required=True,
                                  validators=[UniqueValidator(queryset=User.objects.all())])
    # password = serializers.CharField(write_only=True)
    companyName = serializers.CharField(required=True)
    isInstitution = serializers.BooleanField(required=True)
    isActive = serializers.BooleanField(read_only=True)

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        try:
            with transaction.atomic():
                user = User.objects.create_user(username=validated_data.get('email'),
                                                email=validated_data.get('email'))
                user.first_name = validated_data.get("firstName")
                user.last_name = validated_data.get("lastName")
                # user.set_password(validated_data.get('password'))
                user.set_password('oxit2016')
                user.save()

                group = Group.objects.get(name='Company')
                user.groups.add(group)
                user.save()
                profile = Profile.objects.create(user=user)
                profile.save()
                company = Company(profile=profile)
                company.name = validated_data.get("companyName")
                company.isInstitution = bool(validated_data.get("isInstitution"))
                company.save()
                return company

        except Exception as e:
            traceback.print_exc()
            raise serializers.ValidationError("lütfen tekrar deneyiniz")


class CompanyPageableSerializer(PageSerializer):
    data = CompanySerializer(many=True)

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass
