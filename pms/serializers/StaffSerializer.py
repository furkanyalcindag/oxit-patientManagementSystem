import traceback

from django.contrib.auth.models import User, Group
from rest_framework import serializers

from oxiterp.serializers import UserSerializer
from pms.models import Staff, Profile


class StaffSerializer(serializers.Serializer):

    uuid = serializers.UUIDField(read_only=True)
    user = UserSerializer(read_only=True)
    firstName = serializers.CharField(required=True, write_only=True, allow_blank=False)
    lastName = serializers.CharField(required=True, write_only=True, allow_blank=False)
    username = serializers.CharField(write_only=True, required=False,
                                     )
    # password = serializers.CharField(write_only=True)

    insuranceNumber = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    title = serializers.CharField(read_only=True)
    group = serializers.CharField(write_only=True, label="grup")
    branch = serializers.CharField(allow_null=True, required=False, allow_blank=True)

    def create(self, validated_data):

        user = User.objects.create_user(username=validated_data.get('username'),
                                        email=validated_data.get('username'))
        email = user.email
        password = User.objects.make_random_password()
        user.first_name = validated_data.get("firstName")
        user.last_name = validated_data.get("lastName")
        user.set_password(password)
        user.save()

        try:
            group = Group.objects.get(id=int(validated_data.get("group")))
            user.groups.add(group)
            user.save()
            profile = Profile.objects.create(user=user)
            profile.branch = validated_data.get('branch')
            profile.insuranceNumber = validated_data.get('insuranceNumber')
            profile.title = validated_data.get('title')
            profile.diplomaNo = validated_data.get('diplomaNo')
            profile.save()
            return profile
        except Exception:
            traceback.print_exc()
            user.delete()
            raise serializers.ValidationError("lütfen tekrar deneyiniz")

    def update(self, instance, validated_data):
        try:
            user = instance.user
            user.first_name = validated_data.get("firstName")
            user.last_name = validated_data.get("lastName")
            user.username = validated_data.get("username")
            user.email = validated_data.get("username")
            instance.branch = validated_data.get('branch')
            instance.title = validated_data.get('title')
            instance.diplomaNo = validated_data.get('diplomaNo')
            instance.insuranceNumber = validated_data.get('insuranceNumber')
            user.groups.clear()
            user.groups.add(Group.objects.get(id=int(validated_data.get("group"))))

            user.save()
            instance.save()

            return instance

        except Exception:

            raise serializers.ValidationError("lütfen tekrar deneyiniz")


class UserGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['id', 'name']
