# oxit staff serializer
import traceback

from django.contrib.auth.models import User, Group
from django.db import transaction
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from management.serializers.GeneralSerializer import PageSerializer, SelectSerializer
from pms.models.Patient import Patient
from pms.models.Question import Question


class QuestionSerializer(serializers.Serializer):
    uuid = serializers.UUIDField(read_only=True)
    description = serializers.CharField()
    patient = SelectSerializer(read_only=True)

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        try:
            with transaction.atomic():
                question = Question()
                question.description = validated_data.get('description')
                question.patient = Patient.objects.get(profile__user=self.context['request'].user)
                question.save()
                return question

        except Exception as e:
            traceback.print_exc()
            raise ValidationError("lütfen tekrar deneyiniz")


class QuestionPageableSerializer(PageSerializer):
    data = QuestionSerializer(many=True)
    recordsTotal = serializers.IntegerField()
    recordsFiltered = serializers.IntegerField()
    activePage = serializers.IntegerField()

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass
