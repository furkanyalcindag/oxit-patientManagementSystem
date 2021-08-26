# oxit staff view
import traceback

from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

from management.models.APIObject import APIObject
from pms.models.Assay import Assay
from pms.models.ProtocolAssay import ProtocolAssay
from pms.models.SelectObject import SelectObject
from pmsDoctor.serializers.AssaySerializer import AssaySerializer, AssayPageableSerializer
from pmsDoctor.serializers.GeneralSerializer import SelectSerializer


class AssayApi(APIView):
    def get(self, request, format=None):
        try:
            if request.GET.get('id') is not None:
                assay = Assay.objects.get(uuid=request.GET.get('id'))
                api_object = dict()
                api_object['uuid'] = assay.uuid
                api_object['name'] = assay.name
                api_object['price'] = assay.price
                api_object['taxRate'] = assay.taxRate
                api_object['isPrice'] = assay.isPrice
                serializer = AssaySerializer(api_object, context={'request': request})
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

                data = Assay.objects.filter(name__icontains=name, isDeleted=False).order_by('-id')[
                       lim_start:lim_end]
                filtered_count = Assay.objects.filter(name__icontains=name, isDeleted=False).count()
                arr = []

                for assay in data:
                    api_object = dict()
                    api_object['uuid'] = assay.uuid
                    api_object['name'] = assay.name
                    api_object['price'] = assay.price
                    api_object['taxRate'] = assay.taxRate
                    api_object['isPrice'] = assay.isPrice
                    arr.append(api_object)
                api_object = APIObject()
                api_object.data = arr
                api_object.recordsFiltered = filtered_count
                api_object.recordsTotal = Assay.objects.filter(isDeleted=False).count()
                serializer = AssayPageableSerializer(api_object, context={'request': request})
                return Response(serializer.data, status.HTTP_200_OK)

        except Exception as e:
            traceback.print_exc()
            return Response("", status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request, format=None):
        serializer = AssaySerializer(data=request.data, context={'request', request})
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Assay is created"}, status=status.HTTP_200_OK)
        else:
            errors = dict()
            for key, value in serializer.errors.items():
                if key == 'name':
                    errors['isim'] = value
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, format=None):
        try:
            instance = Assay.objects.get(uuid=request.GET.get('id'))
            serializer = AssaySerializer(data=request.data, instance=instance, context={'request': request})
            if serializer.is_valid():
                serializer.save()
                return Response({'message': "assay is updated"}, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception:
            traceback.print_exc()
            return Response(status.HTTP_400_BAD_REQUEST)

    def delete(self, request, format=None):
        try:
            assay = Assay.objects.get(uuid=request.GET.get('id'))
            assay.isDeleted = True
            assay.save()
            return Response('delete is success', status.HTTP_200_OK)
        except:
            traceback.print_exc()
            return Response(status.HTTP_400_BAD_REQUEST)


class AssaySelectApi(APIView):
    def get(self, request, format=None):
        try:
            select_arr = []
            data = Assay.objects.filter(isDeleted=False)

            for assay in data:
                select_object = SelectObject()
                select_object.value = assay.uuid
                select_object.label = assay.name + ' ' + '(' + str(assay.price) + ' TL)'
                select_arr.append(select_object)

            serializer = SelectSerializer(select_arr, many=True, context={'request': request})

            return Response(serializer.data, status.HTTP_200_OK)
        except Exception as e:
            return Response("error", status.HTTP_500_INTERNAL_SERVER_ERROR)


class PatientAssayApi(APIView):
    def get(self, request, format=None):

        try:
            select_arr = []
            data = ProtocolAssay.objects.filter(protocol__uuid=request.GET.get('id'))

            for d in data:
                select_object = SelectObject()
                select_object.value = d.assay.uuid
                select_object.label = d.assay.name
                select_arr.append(select_object)

            serializer = SelectSerializer(select_arr, many=True, context={'request': request})

            return Response(serializer.data, status.HTTP_200_OK)
        except Exception as e:
            return Response("error", status.HTTP_500_INTERNAL_SERVER_ERROR)
