import traceback

from django.contrib.auth.models import User, Group
from django.db import transaction
from django.db.transaction import atomic
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from pms.models import Profile


class UserSerializer(serializers.Serializer):
    firstName = serializers.CharField()
    lastName = serializers.CharField()
    email = serializers.CharField()
    groupId = serializers.IntegerField(write_only=True)
    groupName = serializers.CharField(read_only=True)
    address = serializers.CharField()
    mobilePhone = serializers.CharField()
    actions = serializers.CharField(read_only=True,required=False)

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        try:
            with transaction.atomic():

                user = User()
                user.first_name = validated_data.get('firstName')
                user.last_name = validated_data.get('lastName')
                user.username = validated_data.get('email')
                user.email = validated_data.get('email')
                user.set_password('oxit2016')
                user.save()

                group = Group.objects.get(id=int(validated_data.get('groupId')))

                user.groups.add(group)
                user.save()

                profile = Profile()
                profile.user = user
                profile.address = validated_data.get('address')
                profile.mobilePhone = validated_data.get('mobilePhone')
                profile.save()

                return user
        except Exception as e:
            raise ValidationError("Lütfen tekrar deneyiniz")
