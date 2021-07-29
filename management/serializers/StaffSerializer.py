# oxit staff serializer
import traceback

from django.contrib.auth.models import User, Group
from django.db import transaction
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework.exceptions import ValidationError

from management.serializers.GeneralSerializer import PageSerializer, SelectSerializer
from pms.models import Profile


class StaffSerializer(serializers.Serializer):
    uuid = serializers.UUIDField(read_only=True)
    firstName = serializers.CharField()
    lastName = serializers.CharField()
    mobilePhone = serializers.CharField()
    email = serializers.CharField()
    group = SelectSerializer(read_only=True)
    groupId = serializers.IntegerField(write_only=True, allow_null=True)

    def update(self, instance, validated_data):
        try:
            with transaction.atomic():

                user = instance.user
                user.firstName = validated_data.get('firstName')
                user.lastName = validated_data.get('lastName')
                user.email = validated_data.get('email')
                user.username = validated_data.get('email')
                user.groups.clear()
                user.groups.add(Group.objects.get(id=validated_data.get('groupId')))
                user.save()
                instance.mobilePhone = validated_data.get('mobilePhone')
                instance.save()

                return instance



        except Exception as e:
            traceback.print_exc()
            raise ValidationError("lütfen tekrar deneyiniz")

    def create(self, validated_data):
        try:
            with transaction.atomic():
                user = User.objects.create_user(username=validated_data.get('email'), email=validated_data.get('email'))
                user.first_name = validated_data.get('firstName')
                user.last_name = validated_data.get('lastName')
                user.set_password('oxit2016')
                y = validated_data.get('groupId')
                user.groups.add(y)
                user.save()
                profile = Profile.objects.create(user=user)
                profile.mobilePhone = validated_data.get('mobilePhone')
                profile.save()
                return profile

        except Exception as e:
            traceback.print_exc()
            raise ValidationError("lütfen tekrar deneyiniz")

    def validate_email(self, email):

        user = None
        if self.instance is not None:

            user = Profile.objects.get(uuid=self.context['request'].query_params['id']).user

            if User.objects.exclude(id=user.id).filter(username=email).count() > 0:
                raise serializers.ValidationError("Bu email sistemde kayıtlıdır")

        else:

            # if isinstance(list(self.context)[0], str):
            #     user = Profile.objects.get(uuid=list(self.context)[1].query_params['id']).user
            # else:
            #     user = Profile.objects.get(uuid=list(self.context)[0].query_params['id']).user
            if User.objects.filter(username=email).count() > 0:
                raise serializers.ValidationError("Bu email sistemde kayıtlıdır")
        return email


class StaffPageableSerializer(PageSerializer):
    data = StaffSerializer(many=True)

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass
