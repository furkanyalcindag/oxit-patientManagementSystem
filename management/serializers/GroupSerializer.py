import traceback

from rest_framework import serializers
from django.contrib.auth.models import Group
from rest_framework.exceptions import ValidationError


class GroupSerializer(serializers.Serializer):
    groupName = serializers.CharField(required=True)

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        try:
            group = Group()
            group.name = validated_data.get('groupName')
            group.save()
            return group
        except Exception as e:
            traceback.print_exc()
            raise ValidationError("Lütfen tekrar deneyiniz")
