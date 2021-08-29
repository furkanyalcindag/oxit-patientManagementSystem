import traceback

from django.db import transaction
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from pms.models import Staff, Appointment, Patient, Department, Blog, Profile
from pmsDoctor.exceptions import AppointmentValidationException
from pmsDoctor.serializers.GeneralSerializer import SelectSerializer, PageSerializer


class BlogSerializer(serializers.Serializer):
    uuid = serializers.UUIDField(read_only=True)
    departmentId = serializers.IntegerField(write_only=True)
    department = SelectSerializer(read_only=True)
    image = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    keyword = serializers.CharField()
    isPublish = serializers.BooleanField(default=False)
    description = serializers.CharField()
    title = serializers.CharField()
    isSponsored = serializers.BooleanField(default=False)

    def update(self, instance, validated_data):
        instance.doctor = Profile.objects.get(user=self.context['request'].user)
        instance.departmentId = Department.objects.get(id=validated_data.get('departmentId'))
        instance.image = validated_data.get('image')
        instance.keyword = validated_data.get('keyword')
        instance.isPublish = validated_data.get('isPublish')
        instance.title = validated_data.get('title')
        instance.description = validated_data.get('description')
        instance.isSponsored = validated_data.get('isSponsored')

        instance.save()

        return instance

    def create(self, validated_data):
        try:
            with transaction.atomic():
                doctor = Profile.objects.get(user=self.context['request'].user)
                blog = Blog()
                blog.department = Department.objects.get(id=validated_data.get('departmentId'))
                blog.doctor = doctor
                blog.image = validated_data.get('image')
                blog.isPublish = validated_data.get('isPublish')
                blog.keyword = validated_data.get('keyword')
                blog.title = validated_data.get('title')
                blog.description = validated_data.get('description')
                blog.isSponsored = validated_data.get('isSponsored')

                blog.save()
                return blog
        except:
            traceback.print_exc()
            raise ValidationError("lütfen tekrar deneyiniz")


class BlogPageSerializer(PageSerializer):
    data = BlogSerializer(many=True)
    recordsTotal = serializers.IntegerField()
    recordsFiltered = serializers.IntegerField()
    activePage = serializers.IntegerField()

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass
