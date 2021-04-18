import traceback

from django.contrib.auth.models import User, Group
from django.db import transaction
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from career.models import Profile, Student
from career.serializers.GeneralSerializers import PageSerializer

from oxiterp.serializers import UserSerializer


class StudentSerializer(serializers.Serializer):
    uuid = serializers.UUIDField(read_only=True)
    user = UserSerializer(read_only=True)
    firstName = serializers.CharField(required=False)
    lastName = serializers.CharField(required=False)
    username = serializers.CharField(write_only=True, required=False,
                                     validators=[UniqueValidator(queryset=User.objects.all())])
    password = serializers.CharField(write_only=True)
    studentNumber = serializers.CharField(required=True)

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        try:
            with transaction.atomic():
                user = User.objects.create_user(username=validated_data.get('username'),
                                                email=validated_data.get('username'))
                user.first_name = validated_data.get("firstName")
                user.last_name = validated_data.get("lastName")
                user.set_password(validated_data.get('password'))
                user.save()

                group = Group.objects.get(name='Student')
                user.groups.add(group)
                user.save()
                profile = Profile.objects.create(user=user)
                profile.save()
                student = Student(profile=profile)
                student.studentNumber = validated_data.get("studentNumber")
                student.isGraduated = False
                student.save()
                return student

        except Exception as e:
            traceback.print_exc()
            raise serializers.ValidationError("lütfen tekrar deneyiniz")


class StudentPageableSerializer(PageSerializer):
    data = StudentSerializer(many=True)
