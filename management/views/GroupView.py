import traceback

from django.contrib.auth.models import Group
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from management.serializers.GeneralSerializer import SelectSerializer


class GroupApi(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):

        try:
            groups = Group.objects.all()

            arr = []

            api_object = dict()
            api_object['label'] = 'Seçiniz'
            api_object['value'] = 0
            arr.append(api_object)
            for group in groups:
                api_object = dict()
                api_object['label'] = group.name
                api_object['value'] = group.id
                arr.append(api_object)

            serializer = SelectSerializer(arr, many=True, context={'request': request})

            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            traceback.print_exc()
            return Response("error", status=status.HTTP_500_INTERNAL_SERVER_ERROR)
