from django.contrib.auth.models import User, Group
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from carService.models.Profile import Profile


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')


class UserAddSerializer(serializers.Serializer):

    uuid = serializers.UUIDField(read_only=True)
    user = UserSerializer(read_only=True)
    gender = serializers.CharField(required=False)
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)
    username = serializers.CharField(write_only=True, required=False,
                                     validators=[UniqueValidator(queryset=User.objects.all())])
    password = serializers.CharField(write_only=True)
    birthDate = serializers.DateField(required=False)
    city = serializers.CharField(required=False)
    mobilePhone = serializers.CharField(required=False)

    def create(self, validated_data):
        
        user = User.objects.create_user(username=validated_data.get('username'),
                                        email=validated_data.get('username'))
        user.first_name = validated_data.get("first_name")
        user.last_name = validated_data.get("last_name")
        user.set_password(validated_data.get('password'))
        user.save()

        try:
            group = Group.objects.get(name='Staff')
            user.groups.add(group)
            user.save()
            profile = Profile.objects.create(user=user
                                             , gender=validated_data.get('gender'))
            profile.mobilePhone = validated_data.get('mobile_phone')
            profile.address = validated_data.get('address')
            profile.save()
            return profile
        except Exception:
            user.delete()
            raise serializers.ValidationError("lütfen tekrar deneyiniz")

    def update(self, instance, validated_data):
        pass