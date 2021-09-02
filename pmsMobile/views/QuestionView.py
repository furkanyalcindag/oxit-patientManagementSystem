# oxit staff view
import traceback

from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

from management.models.APIObject import APIObject
from pms.models.Question import Question
from pmsMobile.serializers.QuestionSerializer import QuestionSerializer, QuestionPageableSerializer


class PatientQuestionApi(APIView):
    def get(self, request, format=None):
        try:
            active_page = 1
            count = 0

            name = ''
            if request.GET.get('activePage') is not None:
                active_page = int(request.GET.get('activePage'))

            lim_start = 10 * (int(active_page) - 1)
            lim_end = lim_start + 10

            data = Question.objects.filter(patient__profile__user=request.user, isDeleted=False).order_by('-id')[
                   lim_start:lim_end]
            count = Question.objects.filter(patient__profile__user=request.user, isDeleted=False).count()
            arr = []

            for question in data:
                api_object = dict()
                api_object['uuid'] = question.uuid
                api_object['description'] = question.description
                arr.append(api_object)
            api_object = APIObject()
            api_object.data = arr
            api_object.recordsFiltered = data.count()
            api_object.recordsTotal = count
            if count % 10 == 0:
                api_object.activePage = count / 10
            else:
                api_object.activePage = (count / 10) + 1
            serializer = QuestionPageableSerializer(api_object, context={'request': request})
            return Response(serializer.data, status.HTTP_200_OK)

        except Exception as e:
            traceback.print_exc()
            return Response("", status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request, format=None):
        serializer = QuestionSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "question is created"}, status=status.HTTP_200_OK)
        else:
            errors = dict()
            for key, value in serializer.errors.items():
                if key == 'description':
                    errors['description'] = value
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, format=None):
        try:
            question = Question.objects.get(uuid=request.GET.get('id'))
            question.isDeleted = True
            question.save()
            return Response('delete is success', status.HTTP_200_OK)
        except:
            traceback.print_exc()
            return Response(status.HTTP_400_BAD_REQUEST)


class AllQuestionApi(APIView):
    def get(self, request, format=None):
        try:
            active_page = 1
            count = 0

            name = ''
            if request.GET.get('activePage') is not None:
                active_page = int(request.GET.get('activePage'))

            lim_start = 10 * (int(active_page) - 1)
            lim_end = lim_start + 10

            data = Question.objects.all().order_by('-id')[
                   lim_start:lim_end]
            count = Question.objects.all().count()
            arr = []

            for question in data:
                api_object = dict()
                api_object['uuid'] = question.uuid
                api_object['description'] = question.description
                arr.append(api_object)
            api_object = APIObject()
            api_object.data = arr
            api_object.recordsFiltered = data.count()
            api_object.recordsTotal = count
            if count % 10 == 0:
                api_object.activePage = count / 10
            else:
                api_object.activePage = (count / 10) + 1
            serializer = QuestionPageableSerializer(api_object, context={'request': request})
            return Response(serializer.data, status.HTTP_200_OK)

        except Exception as e:
            traceback.print_exc()
            return Response("", status.HTTP_500_INTERNAL_SERVER_ERROR)
