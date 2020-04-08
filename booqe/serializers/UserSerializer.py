from django.contrib.auth.models import User, Group
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from booqe.models import Profile
from booqe.serializers.BaseUserSerializer import UserSerializer


class UserRegisterOrGetSerializer(serializers.Serializer):
    # user = serializers.HyperlinkedIdentityField(view_name='patlaks:user-detail', lookup_field='pk')
    id = serializers.IntegerField(read_only=True)
    user = UserSerializer(read_only=True)
    gender = serializers.CharField(required=False)
    #email = serializers.EmailField(write_only=True,required=False, validators=[UniqueValidator(queryset=User.objects.all())])
    first_name = serializers.CharField(required=False, write_only=True)
    last_name = serializers.CharField(write_only=True, required=False)
    # email = serializers.CharField(write_only=True)
    username = serializers.CharField(write_only=True, required=False, validators=[UniqueValidator(queryset=User.objects.all())])
    password = serializers.CharField(write_only=True)
    imei = serializers.CharField(required=False)
    # iban = serializers.CharField(required=False)
    birthDate = serializers.DateField(required=False)
    gcm_registerID = serializers.CharField(write_only=True)
    country = serializers.SlugRelatedField(

        read_only=True,
        slug_field='name'
    )
    # birthYear = serializers.IntegerField(required=False)
    city = serializers.CharField(required=False)
    mobilePhone = serializers.CharField(required=False)

    # country_post = serializers.IntegerField(write_only=True, required=False)
    # reference = serializers.CharField(required=False, allow_blank=True)

    def create(self, validated_data):
        # user_data = validated_data.pop('user')

        # user = User.objects.create(**user_data)

        user = User.objects.create_user(username=validated_data.get('username'),
                                        email=validated_data.get('username'))
        user.set_password(validated_data.get('password'))
        user.save()

        gcm_id = validated_data.get('gcm_registerID')

        imei = validated_data.get('imei')
        # iban = validated_data.get('iban')

        # country = Country.objects.get(pk=validated_data.get('country_post'))
        # birthYear = validated_data.get('birthYear')

        # ref_var = validated_data.get('reference')

        try:

            group = Group.objects.get(name='Member')

            user.groups.add(group)
            user.save()
            profile = Profile.objects.create(user=user
                                             , gcm_registerID=gcm_id)
            profile.save()
            return profile

        except Exception:
            user.delete()
            raise serializers.ValidationError("lütfen tekrar deneyiniz")


class ProfileSerializerFlutter(serializers.Serializer):
    # user = serializers.HyperlinkedIdentityField(view_name='patlaks:user-detail', lookup_field='pk')
    # id = serializers.IntegerField()
    username = serializers.CharField()
    profileImage = serializers.ImageField()
    pinCount = serializers.IntegerField()
    notification = serializers.BooleanField()
    email = serializers.CharField()


class NotificationSerializerFlutter(serializers.Serializer):
    notification = serializers.BooleanField(write_only=True, required=False)

    def create(self, validated_data):
        profile = Profile.objects.get(user=self.context['request'].user)

        p_notification = profile.notification

        if p_notification:
            profile.notification = False

        else:
            profile.notification = True

        profile.save()
        return profile


class PasswordSerializer(serializers.Serializer):
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        user = self.context['request'].user
        ''' user_pk = self.context['request']._request.META['HTTP_AUTHORIZATION'].split(' ')[1]

        decodedPayload = jwt.decode(user_pk, SECRET_KEY)'''
        # user_request = User.objects.get(pk=decodedPayload['user_id'])

        user.set_password(validated_data.get('password'))

        user.save()

        return user


class ProfilePhotoSerializer(serializers.Serializer):
    profileImage = serializers.ImageField(write_only=True)

    def create(self, validated_data):
        user = self.context['request'].user
        ''' user_pk = self.context['request']._request.META['HTTP_AUTHORIZATION'].split(' ')[1]

        decodedPayload = jwt.decode(user_pk, SECRET_KEY)'''
        # user_request = User.objects.get(pk=decodedPayload['user_id'])

        profile = Profile.objects.get(user=user)
        profile.profileImage = validated_data.get('profileImage')

        profile.save()

        return user
