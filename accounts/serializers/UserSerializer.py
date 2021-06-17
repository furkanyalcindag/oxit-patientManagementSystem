import traceback

from django.contrib.auth.models import Group, User
from django.db import transaction
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

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
    id = serializers.CharField(read_only=True)
    email = serializers.EmailField(validators=[UniqueValidator(queryset=User.objects.all())])
    firstName = serializers.CharField()
    lastName = serializers.CharField()
    groupId = serializers.CharField(write_only=True)
    groupName = serializers.CharField(read_only=True)

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        try:
            with transaction.atomic():
                group = Group.objects.get(id=int(validated_data.get('groupId')))

                user = User()
                user.first_name = validated_data.get('firstName')
                user.last_name = validated_data.get('lastName')
                user.email = validated_data.get('email')
                user.username = validated_data.get('email')
                user.set_password('oxit2016')
                user.save()

                user.groups.add(group)
                user.save()

                profile = Profile()
                profile.user = user
                profile.save()

                return profile

        except:
            traceback.print_exc()
            raise serializers.ValidationError("lütfen tekrar deneyiniz")
