from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from carService.serializers.UserSerializer import UserAddSerializer


class UserApi(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, format=None):
        serializer = UserAddSerializer(data=request.data, context={'request': request})

        if serializer.is_valid():
            serializer.save()
            return Response({"message": "user is created"}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
