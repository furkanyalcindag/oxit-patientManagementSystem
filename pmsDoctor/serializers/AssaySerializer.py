# oxit staff serializer
import traceback

from django.contrib.auth.models import User, Group
from django.db import transaction
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from management.serializers.GeneralSerializer import PageSerializer, SelectSerializer
from pms.models import Profile
from pms.models.Assay import Assay


class AssaySerializer(serializers.Serializer):
    uuid = serializers.UUIDField(read_only=True)
    name = serializers.CharField()
    selectName = SelectSerializer(read_only=True)

    def update(self, instance, validated_data):
        try:
            with transaction.atomic():

                instance.name = validated_data.get('name')
                instance.save()
                return instance



        except Exception as e:
            traceback.print_exc()
            raise ValidationError("lütfen tekrar deneyiniz")

    def create(self, validated_data):
        try:
            with transaction.atomic():
                assay = Assay()
                assay.name = validated_data.get('name')
                assay.save()
                return assay

        except Exception as e:
            traceback.print_exc()
            raise ValidationError("lütfen tekrar deneyiniz")



class AssayPageableSerializer(PageSerializer):
    data = AssaySerializer(many=True)

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass
