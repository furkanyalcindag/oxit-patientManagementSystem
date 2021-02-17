from django.contrib.auth.models import Group, User
from django.db.models import Q
from rest_framework import status

from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from carService.models import Profile
from carService.models.SelectObject import SelectObject
from carService.serializers.GeneralSerializer import SelectSerializer
from carService.serializers.UserSerializer import UserAddSerializer, UserGroupSerializer, UserSerializer

#admin
class UserApi(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, format=None):
        serializer = UserAddSerializer(data=request.data, context={'request': request})

        if serializer.is_valid():
            serializer.save()
            return Response({"message": "user is created"}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, format=None):
        users = User.objects.all()
        serialzier = UserSerializer(users, context={'request': request}, many=True)
        return Response(serialzier.data, status.HTTP_200_OK)

#admin
class GroupApi(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        groups = Group.objects.filter(~Q(name='Customer'))
        group_objects = []
        select_object_root = SelectObject()
        select_object_root.label = "Seçiniz"
        select_object_root.value = ""
        group_objects.append(select_object_root)

        for group in groups:
            select_object = SelectObject()
            select_object.label = group.name
            select_object.value = group.id
            group_objects.append(select_object)

        serializer = SelectSerializer(group_objects, many=True, context={'request': request})
        return Response(serializer.data, status.HTTP_200_OK)


class UserPayload(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        user_id = request.user.id
        user = User.objects.get(pk=user_id)
        return Response(user.first_name + ' ' + user.last_name, status.HTTP_200_OK)
