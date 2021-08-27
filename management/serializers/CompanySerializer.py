# oxit staff serializer
import traceback

from django.contrib.auth.models import User, Group
from django.db import transaction
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from management.serializers.GeneralSerializer import PageSerializer, SelectSerializer
from pms.models.Company import Company


class CompanySerializer(serializers.Serializer):
    uuid = serializers.UUIDField(read_only=True)
    companyName = serializers.CharField()
    email = serializers.CharField()
    taxOffice = serializers.CharField()
    taxNumber = serializers.CharField()

    def update(self, instance, validated_data):
        try:
            with transaction.atomic():
                user = instance.user
                user.first_name = validated_data.get('companyName')
                user.email = validated_data.get('email')
                user.save()
                instance.taxOffice = validated_data.get('taxOffice')
                instance.taxNumber = validated_data.get('taxNumber')
                return instance

        except Exception as e:
            traceback.print_exc()
            raise ValidationError("lütfen tekrar deneyiniz")

    def create(self, validated_data):
        try:
            with transaction.atomic():
                user = User.objects.create_user(username=validated_data.get('email'), email=validated_data.get('email'))
                user.first_name = validated_data.get('companyName')
                user.set_password('oxit2016')
                user.groups.add(Group.objects.get(name='Company'))
                user.save()
                company = Company.objects.create(user=user)
                company.taxNumber = validated_data.get('taxNumber')
                company.taxOffice = validated_data.get('taxOffice')
                company.save()
                return company
        except Exception as e:
            traceback.print_exc()
            raise ValidationError("lütfen tekrar deneyiniz")

    def validate_email(self, email):

        user = None
        if self.instance is not None:

            user = Company.objects.get(uuid=self.context['request'].query_params['id']).user

            if User.objects.exclude(id=user.id).filter(username=email).count() > 0:
                raise serializers.ValidationError("Bu email sistemde kayıtlıdır")

        else:
            if User.objects.filter(username=email).count() > 0:
                raise serializers.ValidationError("Bu email sistemde kayıtlıdır")
        return email


class CompanyPageableSerializer(PageSerializer):
    data = CompanySerializer(many=True)

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass
