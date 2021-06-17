import traceback

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from management.models.APIObject import APIObject
from management.serializers.ClinicSerializer import ClinicPageableSerializer, ClinicSerializer
from pms.models import Clinic


class ClinicApi(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):

        try:

            if request.GET.get('id') is not None:

                clinic = Clinic.objects.get(uuid=request.GET.get('id'))

                api_object = dict()
                api_object['clinicName'] = clinic.name
                api_object['taxOffice'] = clinic.taxOffice
                api_object['taxNumber'] = clinic.taxNumber
                api_object['address'] = clinic.address

                api_city_data = dict()
                api_city_data['label'] = clinic.city.name
                api_city_data['value'] = clinic.city.uuid

                api_district_data = dict()
                api_district_data['label'] = clinic.district.name
                api_district_data['value'] = clinic.district.uuid

                api_object['city'] = api_city_data
                api_object['district'] = api_district_data

                serializer = ClinicSerializer(
                    api_object, context={'request': request})

                return Response(serializer.data, status.HTTP_200_OK)
            else:
                active_page = 1
                count = 10

                name = ''

                if request.GET.get('page') is not None:
                    active_page = int(request.GET.get('page'))

                if request.GET.get('name') is not None:
                    name = request.GET.get('name')

                if request.GET.get('count') is not None:
                    count = int(request.GET.get('count'))

                lim_start = count * (int(active_page) - 1)
                lim_end = lim_start + int(count)

                data = Clinic.objects.filter(name__icontains=name, isDeleted=False).order_by('-id')[
                       lim_start:lim_end]

                filtered_count = Clinic.objects.filter(name__icontains=name, isDeleted=False).count()
                arr = []

                for clinic in data:
                    api_object = dict()
                    api_object['clinicName'] = clinic.name
                    api_object['taxOffice'] = clinic.taxOffice
                    api_object['taxNumber'] = clinic.taxNumber
                    api_object['address'] = clinic.address

                    api_city_data = dict()
                    api_city_data['label'] = clinic.city.name
                    api_city_data['value'] = clinic.city.uuid

                    api_district_data = dict()
                    api_district_data['label'] = clinic.district.name
                    api_district_data['value'] = clinic.district.uuid

                    api_object['city'] = api_city_data
                    api_object['district'] = api_district_data
                    arr.append(clinic)

                api_object = APIObject()
                api_object.data = arr
                api_object.recordsFiltered = filtered_count
                api_object.recordsTotal = Clinic.objects.filter(isDeleted=False).count()
                api_object.activePage = 1

                serializer = ClinicPageableSerializer(
                    api_object, context={'request': request})

                return Response(serializer.data, status.HTTP_200_OK)

        except Exception as e:
            traceback.print_exc()
            return Response("", status.HTTP_500_INTERNAL_SERVER_ERROR)
