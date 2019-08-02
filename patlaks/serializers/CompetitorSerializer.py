import datetime

import jwt
from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.relations import PrimaryKeyRelatedField
from rest_framework.response import Response

from oxiterp.serializers import UserSerializer
from oxiterp.settings.base import SECRET_KEY
from patlaks.models import Competitor, Country, Score


class CompetitorSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Competitor
        fields = '__all__'
        depth = 2


class CompetitorSerializer1(serializers.Serializer):
    # user = serializers.HyperlinkedIdentityField(view_name='patlaks:user-detail', lookup_field='pk')
    id = serializers.IntegerField(read_only=True)
    user = UserSerializer(read_only=True)
    gender = serializers.CharField()
    email = serializers.CharField(write_only=True)
    first_name = serializers.CharField(write_only=True)
    # last_name = serializers.CharField(write_only=True, required=False)
    # email = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)
    imei = serializers.CharField(required=False)
    iban = serializers.CharField(required=False)
    birthDate = serializers.DateField(required=False)
    gcm_registerID = serializers.CharField(write_only=True)
    country = serializers.SlugRelatedField(

        read_only=True,
        slug_field='name'
    )
    birthYear = serializers.IntegerField(required=False)
    city = serializers.CharField(required=False)
    mobilePhone = serializers.CharField(required=False)
    country_post = serializers.IntegerField(write_only=True, required=False)
    reference = CompetitorSerializer(read_only=True)

    def create(self, validated_data):
        # user_data = validated_data.pop('user')

        # user = User.objects.create(**user_data)

        user = User.objects.create_user(username=validated_data.get('email'),
                                        first_name=validated_data.get('first_name'),
                                        last_name=validated_data.get('first_name')
                                        , email='xxxxx@xxx.com')
        user.set_password(validated_data.get('password'))
        user.save()
        gender = validated_data.get('gender')
        birthDate = validated_data.get('birthDate')
        imei = validated_data.get('imei')
        iban = validated_data.get('iban')
        gcm = validated_data.get('gcm_registerID')
        # country = Country.objects.get(pk=validated_data.get('country_post'))
        birthYear = validated_data.get('birthYear')
        city = validated_data.get('city')

        competitor = Competitor.objects.create(user=user, gender=gender, gcm_registerID=gcm,
                                               city=city, birth_year=birthYear)

        return competitor


class CompetitorEditSerializer(serializers.Serializer):
    gender = serializers.CharField(required=False)
    email = serializers.CharField(write_only=True, required=False)
    first_name = serializers.CharField(write_only=True, required=False)
    birthYear = serializers.IntegerField(required=False,)
    city = serializers.CharField(required=False)

    def create(self, validated_data):
        user_pk = self.context['request']._request.META['HTTP_AUTHORIZATION'].split(' ')[1]

        decodedPayload = jwt.decode(user_pk, SECRET_KEY)

        user_request = User.objects.get(pk=decodedPayload['user_id'])
        competitor_request = Competitor.objects.get(user=user_request)

        user_request.first_name = validated_data.get('first_name')
        user_request.username = validated_data.get('email')
        competitor_request.gender = validated_data.get('gender')
        competitor_request.birth_year = validated_data.get('birthYear')
        competitor_request.city = validated_data.get('city')
        user_request.save()
        competitor_request.save()

        return competitor_request


class ReferenceSerializer(serializers.Serializer):
    reference_user_name = serializers.CharField(write_only=True)

    def get(self, request, format=None):
        # Model deki veriler, listeye aktarılıyor.

        # Sonuç yollanıyor.
        return Response({"message": "ok"})

    def create(self, validated_data):
        user_pk = self.context['request']._request.META['HTTP_AUTHORIZATION'].split(' ')[1]

        decodedPayload = jwt.decode(user_pk, SECRET_KEY)
        user_request = User.objects.get(pk=decodedPayload['user_id'])
        competitor_request = Competitor.objects.get(user=user_request)
        user_reference = User.objects.get(username=validated_data.get('reference_user_name'))
        competitor_reference = Competitor.objects.get(user=user_reference)
        competitor_request.reference = competitor_reference
        competitor_request.save()

        return competitor_request


class PasswordSerializer(serializers.Serializer):
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        user_pk = self.context['request']._request.META['HTTP_AUTHORIZATION'].split(' ')[1]

        decodedPayload = jwt.decode(user_pk, SECRET_KEY)
        user_request = User.objects.get(pk=decodedPayload['user_id'])

        user_request.set_password(validated_data.get('password'))

        user_request.save()

        return user_request


class ScoreSerializer(serializers.Serializer):
    score = serializers.IntegerField(write_only=True)

    def create(self, validated_data):
        user_pk = self.context['request']._request.META['HTTP_AUTHORIZATION'].split(' ')[1]
        decodedPayload = jwt.decode(user_pk, SECRET_KEY)
        user_request = User.objects.get(pk=decodedPayload['user_id'])
        competitor_request = Competitor.objects.get(user=user_request)

        score = Score(competitor=competitor_request, score=validated_data.get('score'))
        score.save()
        return score


class SelfScoreSerializer(serializers.Serializer):
    score = serializers.IntegerField()
    creationDate = serializers.DateTimeField()


class TopScoreSerializer(serializers.Serializer):
    competitor = CompetitorSerializer()
    score = serializers.IntegerField()
    #creationDate = serializers.DateTimeField()


class CompetitorSerializerReference(serializers.Serializer):
    username = serializers.CharField()