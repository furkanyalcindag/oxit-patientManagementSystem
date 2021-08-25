import traceback

from django.db import transaction
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from pms.models import Staff, Appointment, Patient
from pmsDoctor.exceptions import AppointmentValidationException
from pmsDoctor.serializers.GeneralSerializer import SelectSerializer, PageSerializer


class AppointmentSerializer(serializers.Serializer):
    uuid = serializers.UUIDField(read_only=True)
    patientId = serializers.IntegerField(write_only=True)
    patient = SelectSerializer(read_only=True)
    doctorId = serializers.IntegerField(write_only=True)
    doctor = SelectSerializer(read_only=True)
    date = serializers.DateField()
    time = serializers.TimeField()
    endTime = serializers.TimeField()

    def update(self, instance, validated_data):
        instance.doctor = Staff.objects.get(profile__user_id=validated_data.get('doctorId'))
        instance.patient = Patient.objects.get(profile__user_id=validated_data.get('patientId'))
        instance.date = validated_data.get('date')
        instance.time = validated_data.get('time')
        instance.endTime = validated_data.get('endTime')
        instance.save()

        return instance

    def create(self, validated_data):
        try:
            with transaction.atomic():

                appointment = Appointment()
                doctor = Staff.objects.get(profile__user_id=validated_data.get('doctorId'))
                appointment.patient = Patient.objects.get(profile__user_id=validated_data.get('patientId'))
                date = validated_data.get('date')
                time = validated_data.get('time')
                endTime = validated_data.get('endTime')
                appointments = Appointment.objects.filter(date=date, time=time, endTime=endTime,
                                                          doctor=doctor, isDeleted=False)
                if len(appointments) > 0:
                    raise AppointmentValidationException()
                else:
                    appointment.doctor = doctor
                    appointment.date = date
                    appointment.time = time
                    appointment.endTime = endTime

                    appointment.save()

                    return appointment
        except:
            traceback.print_exc()
            raise ValidationError("lütfen tekrar deneyiniz")


class AppointmentPageSerializer(PageSerializer):
    data = AppointmentSerializer(many=True)

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass


class AppointmentCalendarSerializer(serializers.Serializer):
    uuid = serializers.UUIDField(read_only=True)
    start = serializers.CharField()
    end = serializers.CharField()
    title = serializers.CharField()
    id = serializers.CharField(read_only=False)
    doctorName = serializers.CharField(read_only=True, required=False)

    def to_representation(self, obj):
        return {

            'uuid': obj['uuid'],
            'start': obj['start'],
            'end': obj['end'],
            'title': obj['title'],
            'class': obj['id'],

        }
