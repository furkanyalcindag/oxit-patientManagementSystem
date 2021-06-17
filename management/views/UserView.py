import traceback

from django.contrib.auth.models import Group, User
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from management.serializers.GeneralSerializer import SelectSerializer
from management.serializers.UserSerializer import UserSerializer
from pms.models import Profile


class UserApi(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):

        try:
            users = User.objects.all()
            arr = []
            for user in users:
                profile = Profile.objects.get(user=user)
                api_object = dict()
                api_object['firstName'] = user.first_name
                api_object['lastName'] = user.last_name
                api_object['email'] = user.email
                api_object['groupName'] = Group.objects.get(user=user).name
                api_object['mobilePhone'] = profile.mobilePhone
                api_object['address'] = profile.address
                arr.append(api_object)

            serializer = UserSerializer(arr, many=True, context={'request': request})

            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            traceback.print_exc()
            return Response("error", status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request, format=None):
        serializer = UserSerializer(data=request.data, context={'request': request})

        if serializer.is_valid():
            serializer.save()
            return Response({"message": "user is created"}, status=status.HTTP_200_OK)
        else:
            errors_dict = dict()
            for key, value in serializer.errors.items():
                if key == 'studentNumber':
                    errors_dict['Öğrenci Numarası'] = value

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
