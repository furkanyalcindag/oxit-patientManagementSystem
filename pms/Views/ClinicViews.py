from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from pms.models.APIObject import APIObject
from pms.models import Clinic
from pms.serializers.ClinicSerializer import ClinicSerializer, ClinicPageableSerializer


class ClinicApi(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        data = Clinic.objects.all().order_by('-id')
        arr = []
        for x in data:
            api_data = dict()
            api_data['firstName'] = x.profile.user.first_name
            api_data['lastName'] = x.profile.user.last_name
            api_data['uuid'] = x.uuid
            api_data['clinicName'] = x.name
            api_data['email'] = x.profile.user.username
            api_data['isActive'] = x.profile.user.is_active
            arr.append(api_data)

        api_object = APIObject()
        api_object.data = arr
        api_object.recordsFiltered = data.count()
        api_object.recordsTotal = data.count()
        api_object.activePage = 1

        serializer = ClinicPageableSerializer(
            api_object, context={'request': request})

        return Response(serializer.data, status.HTTP_200_OK)


    def post(self, request, format=None):
        serializer = ClinicSerializer(data=request.data, context={'request': request})

        if serializer.is_valid():
            serializer.save()
            return Response({"message": "clinic is created"}, status=status.HTTP_200_OK)
        else:
            errors_dict = dict()
            for key, value in serializer.errors.items():
                if key == 'name':
                    errors_dict['İsim'] = value
                elif key == 'taxNumber':
                    errors_dict['Vergi Numarası'] = value
                elif key == 'taxOffice':
                    errors_dict['Vergi Dairesi'] = value

            return Response(errors_dict, status=status.HTTP_400_BAD_REQUEST)
