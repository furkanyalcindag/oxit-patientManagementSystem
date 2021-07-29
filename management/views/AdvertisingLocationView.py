import traceback

from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

from management.models.APIObject import APIObject
from management.serializers.AdvertisingLocationSerializer import AdvertisingLocationSerializer, \
    AdvertisingLocationPageableSerializer
from management.serializers.GeneralSerializer import SelectSerializer
from pms.models.AdvertisingLocation import AdvertisingLocation
from pms.models.SelectObject import SelectObject


class AdvertisingLocationApi(APIView):
    def get(self, request, format=None):
        try:
            if request.GET.get('id') is not None:
                advertising = AdvertisingLocation.objects.get(uuid=request.GET.get('id'))
                api_object = dict()
                api_object['uuid'] = advertising.uuid
                api_object['name'] = advertising.name
                api_object['width'] = advertising.width
                api_object['height'] = advertising.height
                serializer = AdvertisingLocationSerializer(api_object, context={'request': request})
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
                data = AdvertisingLocation.objects.filter(name__icontains=name, isDeleted=False).order_by(
                    '-id')[
                       lim_start:lim_end]
                filtered_count = AdvertisingLocation.objects.filter(name__icontains=name,
                                                                    isDeleted=False).count()
                arr = []
                for d in data:
                    api_object = dict()
                    api_object['uuid'] = d.uuid
                    api_object['name'] = d.name
                    api_object['width'] = d.width
                    api_object['height'] = d.height
                    arr.append(api_object)
                api_object = APIObject()
                api_object.data = arr
                api_object.recordsFiltered = filtered_count
                api_object.recordsTotal = AdvertisingLocation.objects.filter(isDeleted=False).count()
                serializer = AdvertisingLocationPageableSerializer(api_object, context={'request': request})
                return Response(serializer.data, status.HTTP_200_OK)
        except Exception as e:
            traceback.print_exc()
            return Response("", status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request, format=None):
        serializer = AdvertisingLocationSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "company is created"}, status.HTTP_200_OK)
        else:
            errors = dict()
            for key, value in serializer.errors.items():
                if key == 'name':
                    errors['name'] = value
                elif key == 'width':
                    errors['width'] = value
                elif key == 'height':
                    errors['height'] = value
            return Response(errors, status.HTTP_400_BAD_REQUEST)

    def put(self, request, format=None):
        try:
            instance = AdvertisingLocation.objects.get(uuid=request.GET.get('id'))
            serializer = AdvertisingLocationSerializer(data=request.data, instance=instance,
                                                       context={'request', request})

            if serializer.is_valid():
                serializer.save()
                return Response({'message': 'company is updated'}, status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            traceback.print_exc()
            return Response(status.HTTP_400_BAD_REQUEST)

    def delete(self, request, format=None):
        try:
            company = AdvertisingLocation.objects.get(uuid=request.GET.get('id'))
            company.isDeleted = True
            company.save()
            return Response('delete is succes', status.HTTP_200_OK)
        except Exception as e:
            traceback.print_exc()
            return Response(status.HTTP_400_BAD_REQUEST)


class AdvertisingLocationSelectApi(APIView):
    def get(self, request, format=None):
        try:
            data = AdvertisingLocation.objects.filter(isDeleted=False)
            arr = []
            for d in data:
                select_object = SelectObject()
                select_object.label = d.name
                select_object.value = d.id
                arr.append(select_object)
            serializer = SelectSerializer(arr, many=True, context={'request': request})
            return Response(serializer.data, status.HTTP_200_OK)
        except:
            return Response("error", status.HTTP_500_INTERNAL_SERVER_ERROR)
