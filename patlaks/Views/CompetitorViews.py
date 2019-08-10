import calendar
from datetime import datetime

import jwt
from django.contrib.auth.models import User
from django.db.models import Min
from pytz import unicode
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.test import APIRequestFactory
from rest_framework.views import APIView

from oxiterp.settings.base import SECRET_KEY
from patlaks.models import Competitor, Score
from patlaks.models.Message import Message
from patlaks.serializers.CompetitorSerializer import CompetitorSerializer, CompetitorSerializer1, ReferenceSerializer, \
    ScoreSerializer, SelfScoreSerializer, TopScoreSerializer, CompetitorSerializerReference, PasswordSerializer, \
    CompetitorEditSerializer, MessageSerializer, CompetitorNotificationSerializer, BankInformationSerializer, \
    PasswordForgotSerializer, GCMTokenSerializer


class CompetitorList(APIView):

    def get(self, request, format=None):
        content = {
            'user': unicode(request.user),  # `django.contrib.auth.User` instance.
            'auth': unicode(request.auth),  # None
        }
        competitors = Competitor.objects.all()
        serializer = CompetitorSerializer(competitors, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = CompetitorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CompetitorGet(APIView):
    def get(self, request, format=None):
        user_pk = request.user.id

        user_request = User.objects.get(pk=user_pk)
        competitor_request = Competitor.objects.get(user=user_request)
        serializer_context = {
            'request': request,
        }
        serializer = CompetitorSerializer(competitor_request, context=serializer_context)
        return Response(serializer.data)


class NotificationGet(APIView):
    def get(self, request, format=None):
        user_pk = request.user.id

        user_request = User.objects.get(pk=user_pk)
        competitor_request = Competitor.objects.get(user=user_request)
        serializer_context = {
            'request': request,
        }
        serializer = CompetitorNotificationSerializer(competitor_request, context=serializer_context)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = CompetitorNotificationSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Notification settings changed"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# yarışmacı oluşturma
class CreateCompetitor(APIView):

    def get(self, request, format=None):
        competitors = Competitor.objects.all()
        serializer_context = {
            'request': request,
        }
        serializer = CompetitorSerializer1(competitors, many=True, context=serializer_context)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = CompetitorSerializer1(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User created"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# referans ekleme
class AddReference(APIView):

    def post(self, request, format=None):
        serializer = ReferenceSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Reference added"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# referans ekleme
class ChangePassword(APIView):

    def post(self, request, format=None):
        serializer = PasswordSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Password Changed"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# referans ekleme
class ForgotPassword(APIView):

    def post(self, request, format=None):
        serializer = PasswordForgotSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "new password sent to your mail"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# referans ekleme
class GCMTokenUpdate(APIView):

    def post(self, request, format=None):
        serializer = GCMTokenSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Token is updated"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UpdateCompetitor(APIView):

    def post(self, request, format=None):
        serializer = CompetitorEditSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Competitor was updated"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # skor ekleme


class UpdateBank(APIView):
    def get(self, request, format=None):
        user_pk = request.user.id

        user_request = User.objects.get(pk=user_pk)
        competitor_request = Competitor.objects.get(user=user_request)
        serializer_context = {
            'request': request,
            'first_name': user_request.first_name,
            'iban': competitor_request.iban

        }
        array = []

        yourdata = [{"first_name": user_request.first_name, "iban": competitor_request.iban}]

        # array.append({'iban': competitor_request.iban, 'first_name': user_request.first_name})
        serializer = BankInformationSerializer(yourdata,many=True, context=serializer_context)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = BankInformationSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Competitor was updated"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AddScore(APIView):

    def post(self, request, format=None):
        serializer = ScoreSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            s = serializer.save()
            datetime_current = datetime.today()
            year = datetime_current.year
            month = datetime_current.month
            num_days = calendar.monthrange(year, month)[1]

            datetime_start = datetime(year, month, 1, 0, 0)

            datetime_end = datetime(year, month, num_days, 23, 59)

            # competitor_request = Competitor.objects.get(user=user_request)
            # scores = Score.objects.filter(creationDate__range=(datetime_start, datetime_end)).order_by('score')[:100]
            scores = Score.objects.filter(creationDate__range=(datetime_start, datetime_end)).values(
                'competitor').annotate(score=Min('score')).order_by('score')[:100]
            i = 1
            for score in scores:
                if score.id == s.id:
                    return Response({"message": "Score added", "rank": i}, status=status.HTTP_201_CREATED)
                i += 1

            return Response({"message": "Score added", "is_rank": False}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# yarışmacı skoru
class GetCompetitorScore(APIView):

    def get(self, request, format=None):
        user_pk = request.user.id

        user_request = User.objects.get(pk=user_pk)
        competitor_request = Competitor.objects.get(user=user_request)
        scores = Score.objects.filter(competitor=competitor_request).order_by('score')[:10]
        serializer_context = {
            'request': request,
        }
        serializer = SelfScoreSerializer(scores, many=True, context=serializer_context)
        return Response(serializer.data)


# yarışmacı skoru
class GetCompetitorMessage(APIView):

    def get(self, request, format=None):
        user_pk = request.user.id

        user_pk = request._request.META['HTTP_AUTHORIZATION'].split(' ')[1]
        decodedPayload = jwt.decode(user_pk, SECRET_KEY)
        user_request = User.objects.get(pk=decodedPayload['user_id'])
        # user_request = User.objects.get(pk=user_pk)
        competitor_request = Competitor.objects.get(user=user_request)
        messages = Message.objects.filter(to=competitor_request)
        serializer_context = {
            'request': request,
        }
        serializer = MessageSerializer(messages, many=True, context=serializer_context)
        return Response(serializer.data)


# top 100 skor
class GetTop100(APIView):

    def get(self, request, format=None):
        user_pk = request.user.id
        datetime_current = datetime.today()
        year = datetime_current.year
        month = datetime_current.month
        num_days = calendar.monthrange(year, month)[1]

        datetime_start = datetime(year, month, 1, 0, 0)

        datetime_end = datetime(year, month, num_days, 23, 59)

        user_request = User.objects.get(pk=user_pk)
        # competitor_request = Competitor.objects.get(user=user_request)
        # scores = Score.objects.filter(creationDate__range=(datetime_start, datetime_end)).order_by('score')[:100]
        serializer_context = {
            'request': request,
        }

        scores = Score.objects.filter(creationDate__range=(datetime_start, datetime_end)).values(
            'competitor').annotate(score=Min('score')).order_by('score')[:100]

        my_objects = []

        for score in scores:
            new = Competitor.objects.get(id=score['competitor'])
            newScore = Score()
            newScore.competitor = new
            newScore.score = score['score']
            my_objects.append(newScore)

        serializer = TopScoreSerializer(my_objects, many=True, context=serializer_context)

        return Response(serializer.data)


# alt üyeleri getir
class GetChildrenCompetitors(APIView):
    def get(self, request, format=None):
        user_pk = request.user.id

        user_request = User.objects.get(pk=user_pk)
        competitor_request = Competitor.objects.get(user=user_request)
        competitors = Competitor.objects.filter(reference=competitor_request)

        username = []

        for competitor in competitors:
            username.append({'username': competitor.user.username})

        serializer = CompetitorSerializerReference(username, many=True)
        return Response(serializer.data)
