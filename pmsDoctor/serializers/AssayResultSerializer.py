# oxit staff serializer
import traceback

from django.contrib.auth.models import User, Group
from django.db import transaction
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from management.serializers.GeneralSerializer import PageSerializer, SelectSerializer
from pms.models import Profile


class AssayResultSerializer(serializers.Serializer):
    uuid = serializers.UUIDField(read_only=True)
    result = serializers.CharField()
    assay = SelectSerializer(read_only=True)
    patient = SelectSerializer(read_only=True)

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass
