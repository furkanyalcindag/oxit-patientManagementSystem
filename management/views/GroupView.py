import traceback

from django.contrib.auth.models import Group
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from management.serializers.GroupSerializer import GroupSerializer
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

    def post(self, request, format=None):
        serializer = GroupSerializer(data=request.data, context={'request': request})

        if serializer.is_valid():
            serializer.save()
            return Response({"message": "group is created"}, status=status.HTTP_200_OK)
        else:
            errors = dict()
            for key, value in serializer.errors.items():
                if key == 'groupName':
                    errors['Group Adı'] = value
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, format=None):
        try:
            group = Group.objects.get(id=request.GET.get('id'))
            group.delete()
            return Response('delete is success', status.HTTP_200_OK)
        except:
            traceback.print_exc()
            return Response(status.HTTP_400_BAD_REQUEST)
