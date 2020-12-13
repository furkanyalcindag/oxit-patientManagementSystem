from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from carService.models import Service, Car
from carService.models.ApiObject import APIObject
from carService.models.SelectObject import SelectObject
from carService.models.ServiceType import ServiceType
from carService.serializers.GeneralSerializer import SelectSerializer
from carService.serializers.ServiceSerializer import ServicePageSerializer, ServiceSerializer


class ServiceApi(APIView):
    # permission_classes = (IsAuthenticated,)
    def get(self, request, format=None):
        data = Service.objects.filter(car=Car.objects.get(uuid=request.GET.get('carId'))).order_by('-id')
        api_object = APIObject()
        api_object.data = data
        api_object.recordsFiltered = data.count()
        api_object.recordsTotal = data.count()
        serializer = ServicePageSerializer(api_object, context={'request': request})
        return Response(serializer.data, status.HTTP_200_OK)

    def post(self, request, format=None):

        serializer = ServiceSerializer(data=request.data, context={'request': request})

        if serializer.is_valid():
            serializer.save()
            return Response({"message": "service is created"}, status=status.HTTP_200_OK)
        else:

            errors_dict = dict()
            for key, value in serializer.errors.items():
                if key == 'serviceType':
                    errors_dict['Servis Tipi'] = value
                elif key == 'serviceKM':
                    errors_dict['KM'] = value
                elif key == 'complaint':
                    errors_dict['Şikayet'] = value
                elif key == 'responsiblePerson':
                    errors_dict['Sorumlu Kişi'] = value

            return Response(errors_dict, status=status.HTTP_400_BAD_REQUEST)


class ServiceTypeSelectApi(APIView):
    # permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        service_types = ServiceType.objects.all()
        service_types_objects = []

        for service_type in service_types:
            select_object = SelectObject()
            select_object.label = service_type.name
            select_object.value = service_type.id
            service_types_objects.append(select_object)

        serializer = SelectSerializer(service_types_objects, many=True, context={'request': request})
        return Response(serializer.data, status.HTTP_200_OK)
