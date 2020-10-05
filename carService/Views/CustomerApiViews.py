from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from carService.models import Profile
from carService.serializers.UserSerializer import CustomerAddSerializer


class CustomerApi(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        data = Profile.objects.filter(user__groups__name__iexact='Customer')
        serializer = CustomerAddSerializer(data, many=True, context={'request': request})
        return Response(serializer.data, status.HTTP_200_OK)

    def post(self, request, format=None):
        serializer = CustomerAddSerializer(data=request.data, context={'request': request})

        if serializer.is_valid():
            serializer.save()
            return Response({"message": "user is created"}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

