# oxit staff serializer
import traceback

from django.db import transaction
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from management.serializers.GeneralSerializer import PageSerializer
from pms.models.Staff import Staff
from pms.models.Answer import Answer
from pms.models.Patient import Patient
from pms.models.Question import Question
from pms.models.QuestionsAnswers import QuestionsAnswers


class AnswerSerializer(serializers.Serializer):
    uuid = serializers.UUIDField(read_only=True)
    description = serializers.CharField()

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        try:
            with transaction.atomic():
                answer = Answer()
                answer.description = validated_data.get('description')
                if self.context['request'].user.groups.values('name')[0]['name'] == 'Patient':
                    answer.patient = Patient.objects.get(profile__user=self.context['request'].user)
                else:
                    answer.doctor = Staff.objects.get(profile__user=self.context['request'].user)
                answer.save()

                questionAnswers = QuestionsAnswers()
                questionAnswers.answer = answer
                questionAnswers.question = Question.objects.get(uuid=self.context['request'].GET.get('questionId'))
                questionAnswers.save()
                return answer

        except Exception as e:
            traceback.print_exc()
            raise ValidationError("lütfen tekrar deneyiniz")


class AnswerPageableSerializer(PageSerializer):
    data = AnswerSerializer(many=True)

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass
