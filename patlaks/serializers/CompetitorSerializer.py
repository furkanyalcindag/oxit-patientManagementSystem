import datetime

import jwt
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.http import Http404
from rest_framework import serializers
from rest_framework.relations import PrimaryKeyRelatedField
from rest_framework.response import Response
from rest_framework.validators import UniqueValidator

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
    email = serializers.CharField(write_only=True, validators=[UniqueValidator(queryset=User.objects.all())])
    # first_name = serializers.CharField(required=False, write_only=True)
    # last_name = serializers.CharField(write_only=True, required=False)
    # email = serializers.CharField(write_only=True)
    username = serializers.CharField()
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
    reference = serializers.CharField(required=False)

    def create(self, validated_data):
        # user_data = validated_data.pop('user')

        # user = User.objects.create(**user_data)

        user = User.objects.create_user(username=validated_data.get('username'),
                                        first_name=validated_data.get('username'),
                                        last_name=validated_data.get('username')
                                        , email=validated_data.get('email'))
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

        if validated_data.get('reference') is None:
            competitor = Competitor.objects.create(user=user, gender=gender, gcm_registerID=gcm,
                                                   city=city, birth_year=birthYear, reference_count=0)
        else:
            try:
                userc = User.objects.get(username=validated_data.get('reference'))
                competitorc = Competitor.objects.get(user=userc)
                competitor = Competitor.objects.create(user=user, gender=gender, gcm_registerID=gcm,
                                                       city=city, birth_year=birthYear, reference=competitorc)
                competitor.reference_count = 1
                competitor.save()
            except:
                user.delete()
                user.save()

        return competitor


class BankInformationSerializer(serializers.Serializer):
    first_name = serializers.CharField()
    iban = serializers.CharField()

    def create(self, validated_data):
        user_pk = self.context['request']._request.META['HTTP_AUTHORIZATION'].split(' ')[1]

        decodedPayload = jwt.decode(user_pk, SECRET_KEY)

        user_request = User.objects.get(pk=decodedPayload['user_id'])
        competitor_request = Competitor.objects.get(user=user_request)

        user_request.first_name = validated_data.get('first_name')
        user_request.save()
        competitor_request.iban = validated_data.get('iban')
        competitor_request.save()
        return competitor_request


class CompetitorEditSerializer(serializers.Serializer):
    gender = serializers.CharField(required=False)
    email = serializers.CharField(write_only=True, required=False)
    # first_name = serializers.CharField(write_only=True, required=False)
    birthYear = serializers.IntegerField(required=False, )
    city = serializers.CharField(required=False)
    username = serializers.CharField()

    def create(self, validated_data):
        user_pk = self.context['request']._request.META['HTTP_AUTHORIZATION'].split(' ')[1]

        decodedPayload = jwt.decode(user_pk, SECRET_KEY)

        user_request = User.objects.get(pk=decodedPayload['user_id'])
        competitor_request = Competitor.objects.get(user=user_request)

        # user_request.first_name = validated_data.get('first_name')
        user_request.username = validated_data.get('username')
        user_request.email = validated_data.get('email')
        competitor_request.gender = validated_data.get('gender')
        competitor_request.birth_year = validated_data.get('birthYear')
        competitor_request.city = validated_data.get('city')
        user_request.save()
        competitor_request.save()

        return competitor_request


class CompetitorNotificationSerializer(serializers.Serializer):
    notification = serializers.BooleanField()

    def create(self, validated_data):
        user_pk = self.context['request']._request.META['HTTP_AUTHORIZATION'].split(' ')[1]

        decodedPayload = jwt.decode(user_pk, SECRET_KEY)

        user_request = User.objects.get(pk=decodedPayload['user_id'])
        competitor_request = Competitor.objects.get(user=user_request)
        competitor_request.notification = validated_data.get('notification')
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
        if competitor_request.reference_count < 2:

            user_reference = User.objects.get(username=validated_data.get('reference_user_name'))
            if competitor_request.user is user_reference:
                serializers.ValidationError("self reference")
            else:

                if competitor_request is Competitor.objects.get(reference=user_reference).reference:
                    serializers.ValidationError("looping reference")
                else:
                    competitor_reference = Competitor.objects.get(user=user_reference)
                    competitor_request.reference = competitor_reference
                    competitor_request.reference_count = competitor_request.reference_count + 1
                    competitor_request.save()
        else:
            serializers.ValidationError("limited reference")

        return competitor_request


class PasswordForgotSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)

    def create(self, validated_data):
        try:
            user = User.objects.get(email=validated_data.get('email'))
            password = User.objects.make_random_password()
            user.set_password(password)
            user.save()
            res = send_mail("Reset Password-Patlaks", "Yeni şifreniz :" + password, "register@eymo.net",
                            [user.email])
            return res

        except User.DoesNotExist:
            raise Http404("Girilen maile ait bir kullanıcı bulunamadı.")


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


class GCMTokenSerializer(serializers.Serializer):
    gcm_registerID = serializers.CharField(write_only=True)

    def create(self, validated_data):
        user_pk = self.context['request']._request.META['HTTP_AUTHORIZATION'].split(' ')[1]
        decodedPayload = jwt.decode(user_pk, SECRET_KEY)
        user_request = User.objects.get(pk=decodedPayload['user_id'])
        competitor_request = Competitor.objects.get(user=user_request)
        competitor_request.gcm_registerID = validated_data.get('gcm_registerID')

        competitor_request.save()
        return competitor_request


class SelfScoreSerializer(serializers.Serializer):
    score = serializers.IntegerField()
    creationDate = serializers.DateTimeField()


class MessageSerializer(serializers.Serializer):
    body = serializers.CharField()
    creationDate = serializers.DateTimeField()


class TopScoreSerializer(serializers.Serializer):
    competitor = CompetitorSerializer()
    score = serializers.IntegerField()
    # creationDate = serializers.DateTimeField()


class CompetitorSerializerReference(serializers.Serializer):
    username = serializers.CharField()
