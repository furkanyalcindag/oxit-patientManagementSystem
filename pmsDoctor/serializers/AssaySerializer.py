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
    taxRate = serializers.DecimalField(max_digits=10, decimal_places=2)
    price = serializers.DecimalField(max_digits=10, decimal_places=2)
    isPrice = serializers.BooleanField(default=False)

    def update(self, instance, validated_data):
        try:
            with transaction.atomic():

                instance.name = validated_data.get('name')
                instance.isPrice = validated_data.get('isPrice')
                if not instance.isPrice:
                    instance.price = 0
                    instance.taxRate = 0
                else:
                    instance.price = validated_data.get('price') + (validated_data.get('price') * validated_data.get(
                        'taxRate') / 100)
                    instance.taxRate = validated_data.get('taxRate')
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
                assay.isPrice = validated_data.get('isPrice')
                if not assay.isPrice:
                    assay.price = 0
                    assay.taxRate = 0
                else:
                    assay.taxRate = validated_data.get('taxRate')
                    assay.price = validated_data.get('price') + (validated_data.get('price') * validated_data.get(
                        'taxRate') / 100)
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
