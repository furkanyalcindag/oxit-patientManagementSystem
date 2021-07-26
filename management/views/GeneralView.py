from rest_framework import status
from rest_framework.views import APIView

from management.serializers.GeneralSerializer import SelectSerializer
from pms.models import District, City
from pms.models.SelectObject import SelectObject
from rest_framework.response import Response


class CityDistrictSelectApi(APIView):
    def get(self, request, format=None):
        try:
            select_arr = []
            if request.GET.get('id') is not None:
                data = District.objects.filter(city=City.objects.get(id=request.GET.get('id')))

                for district in data:
                    select_object = SelectObject
                    select_object.value = district.id
                    select_object.label = district.name
                    select_arr.append(select_object)
            else:
                data = City.objects.all()

                for city in data:
                    select_object = SelectObject()
                    select_object.value = city.id
                    select_object.label = city.name
                    select_arr.append(select_object)

            serializer = SelectSerializer(select_arr, many=True, context={'request': request})

            return Response(serializer.data, status.HTTP_200_OK)
        except Exception as e:
            return Response("error", status.HTTP_500_INTERNAL_SERVER_ERROR)
