import traceback

from django.contrib.auth.models import Group, User
from django.db import transaction
from keyring.backends import null
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.validators import UniqueValidator

from accounts.exceptions import PasswordConfirmException, PasswordValidationException
from pms.models import Patient
from pms.models.BloodGroup import BloodGroup
from pms.models.Gender import Gender
from pms.models.Profile import Profile


class GroupSerializer(serializers.Serializer):
    groupName = serializers.CharField()
    id = serializers.IntegerField(read_only=True)

    def update(self, instance, validated_data):
        try:
            instance.name = validated_data('groupName')
            instance.save()
        except:
            traceback.print_exc()
            raise serializers.ValidationError("lütfen tekrar deneyiniz!")

    def create(self, validated_data):
        try:
            group = Group()
            group.name = validated_data.get('groupName')
            group.save()

            # show_urls_by_group(urls.urlpatterns, group, depth=0)
            return group
        except:
            traceback.print_exc()
            raise serializers.ValidationError("lütfen tekrar deneyiniz!")


class UserSerializer(serializers.Serializer):
    email = serializers.EmailField(validators=[UniqueValidator(queryset=User.objects.all())])
    firstName = serializers.CharField()
    lastName = serializers.CharField()
    password = serializers.CharField()
    genderId = serializers.IntegerField()
    bloodGroupId = serializers.IntegerField()
    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        try:
            with transaction.atomic():

                user = User.objects.create_user(email=validated_data.get('email'), username=validated_data.get('email'),
                                                password=validated_data.get('password'))
                user.save()
                user.first_name = validated_data.get('firstName')
                user.last_name = validated_data.get('lastName')
                user.groups.add(Group.objects.get(name='Patient'))
                user.save()
                profile = Profile.objects.create(user=user)
                profile.save()
                patient = Patient.objects.create(profile=profile)
                patient.gender = Gender.objects.get(id=validated_data.get('genderId'))
                patient.bloodGroup = BloodGroup.objects.get(id=validated_data.get('bloodGroupId'))
                # patient.birthDate = validated_data.get('birthDate')
                patient.save()
                return user
        except Exception as e:
            raise ValidationError("Lütfen tekrar deneyiniz")


class PasswordChangeSerializer(serializers.Serializer):
    confirmPassword = serializers.CharField()
    password = serializers.CharField()

    def update(self, instance, validated_data):
        try:
            password = validated_data.get('password')
            confirm = validated_data.get('confirmPassword')

            if password != confirm:
                raise PasswordConfirmException()

            if len(password) < 6:
                raise PasswordValidationException()

            instance.set_password(validated_data.get('password'))
            instance.save()
            return instance
        except PasswordConfirmException:
            traceback.print_exc()
            raise serializers.ValidationError("Şifreler eşleşmiyor")

        except PasswordValidationException:
            traceback.print_exc()
            raise serializers.ValidationError("En az 6 karakter olmalı")
        except Exception:
            traceback.print_exc()
            raise serializers.ValidationError("lütfen tekrar deneyiniz")

    def create(self, validated_data):
        pass
