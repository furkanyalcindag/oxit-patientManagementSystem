from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from career.models import Company
from career.models.APIObject import APIObject
from career.serializers.CompanySerializer import CompanyPageableSerializer, CompanySerializer


class CompanyApi(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        data = Company.objects.all().order_by('-id')
        arr = []
        for x in data:
            api_data = dict()
            api_data['firstName'] = x.profile.user.first_name
            api_data['lastName'] = x.profile.user.last_name
            api_data['uuid'] = x.uuid
            api_data['companyName'] = x.name
            api_data['email'] = x.profile.user.username
            api_data['isInstitution'] = x.isInstitution
            arr.append(api_data)

        api_object = APIObject()
        api_object.data = arr
        api_object.recordsFiltered = data.count()
        api_object.recordsTotal = data.count()
        api_object.activePage = 1

        serializer = CompanyPageableSerializer(
            api_object, context={'request': request})

        return Response(serializer.data, status.HTTP_200_OK)

    def post(self, request, format=None):
        serializer = CompanySerializer(data=request.data, context={'request': request})

        if serializer.is_valid():
            serializer.save()
            return Response({"message": "company is created"}, status=status.HTTP_200_OK)
        else:
            errors_dict = dict()
            for key, value in serializer.errors.items():
                if key == 'studentNumber':
                    errors_dict['Öğrenci Numarası'] = value

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
