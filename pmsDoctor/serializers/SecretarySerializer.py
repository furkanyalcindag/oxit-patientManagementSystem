# oxit staff serializer
import traceback

from django.contrib.auth.models import User, Group
from django.db import transaction
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from management.serializers.GeneralSerializer import PageSerializer, SelectSerializer
from pms.models import Profile


class SecretarySerializer(serializers.Serializer):
    uuid = serializers.UUIDField(read_only=True)
    firstName = serializers.CharField()
    lastName = serializers.CharField()
    email = serializers.CharField()

    def update(self, instance, validated_data):
        try:
            with transaction.atomic():

                user = instance.user
                user.first_name = validated_data.get('firstName')
                user.last_name = validated_data.get('lastName')
                user.email = validated_data.get('email')
                user.username = validated_data.get('email')
                user.save()
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
                group = Group.objects.get(name='Secretary')
                user.groups.add(group)
                user.save()
                profile = Profile.objects.create(user=user)
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
            if User.objects.filter(username=email).count() > 0:
                raise serializers.ValidationError("Bu email sistemde kayıtlıdır")
        return email


class SecretaryPageableSerializer(PageSerializer):
    data = SecretarySerializer(many=True)
    recordsTotal = serializers.IntegerField()
    recordsFiltered = serializers.IntegerField()
    activePage = serializers.IntegerField()

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass
