# oxit staff view
import traceback

from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

from management.models.APIObject import APIObject
from pms.models.Assay import Assay
from pms.models.Protocol import Protocol
from pmsDoctor.serializers.AssaySerializer import AssaySerializer, AssayPageableSerializer
from pmsDoctor.serializers.ProtocolSerializer import ProtocolSerializer, ProtocolPageableSerializer


class ProtocolApi(APIView):
    def get(self, request, format=None):
        try:
            if request.GET.get('id') is not None:
                protocol = Protocol.objects.filter(patient__uuid=request.GET.get('id'))
                api_object = dict()
                arr=[]
                for data in protocol:
                    api_object['uuid'] = data.uuid
                    api_object['description'] = data.description
                    api_patient_data = dict()
                    api_patient_data['label'] = data.patient.profile.user.first_name
                    api_patient_data['value'] = data.patient.id
                    api_object['patient'] = api_patient_data
                    arrayAssay = []
                    for assay in Assay.objects.filter(name=data.assay.name):
                        api_assay_data = dict()
                        api_assay_data['name'] = assay.name
                        api_assay_data['uuid'] = assay.uuid
                        arrayAssay.append(api_assay_data)
                    api_object['assayList'] = arrayAssay
                    arr.append(api_object)
                serializer = ProtocolSerializer(arr, context={'request': request})
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

                data = Protocol.objects.filter(patient__profile__user__first_name__icontains=name,
                                            isDeleted=False).order_by('-id')[
                       lim_start:lim_end]
                filtered_count = Protocol.objects.filter(patient__profile__user__first_name__icontains=name,
                                                      isDeleted=False).count()
                arr = []

                for protocol in data:
                    api_object = dict()
                    api_object['uuid'] = protocol.uuid
                    api_object['description'] = protocol.description
                    api_object['assay'] = protocol.description
                    api_patient_data = dict()
                    api_patient_data['label'] = protocol.patient.profile.user.first_name
                    api_patient_data['value'] = protocol.patient.id
                    api_object['patient'] = api_patient_data

                    arrayAssay = []
                    for assay in Assay.objects.filter(name=protocol.assay.name):
                        api_assay_data = dict()
                        api_assay_data['name'] = assay.name
                        api_assay_data['uuid'] = assay.uuid
                        arrayAssay.append(api_assay_data)
                    api_object['assayList'] = arrayAssay
                    arr.append(api_object)
                api_object = APIObject()
                api_object.data = arr
                api_object.recordsFiltered = filtered_count
                api_object.recordsTotal = Protocol.objects.filter(isDeleted=False).count()
                serializer = ProtocolPageableSerializer(api_object, context={'request': request})
                return Response(serializer.data, status.HTTP_200_OK)

        except Exception as e:
            traceback.print_exc()
            return Response("", status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request, format=None):
        serializer = ProtocolSerializer(data=request.data, context={'request', request})
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Assay is created"}, status=status.HTTP_200_OK)
        else:
            errors = dict()
            for key, value in serializer.errors.items():
                if key == 'description':
                    errors['description'] = value
                elif key == 'assayId':
                    errors['assay'] = value
                elif key == 'patientId':
                    errors['patientId'] = value
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, format=None):
        try:
            instance = Protocol.objects.get(uuid=request.GET.get('id'))
            serializer = ProtocolSerializer(data=request.data, instance=instance, context={'request': request})
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
            protocol = Protocol.objects.get(uuid=request.GET.get('id'))
            protocol.isDeleted = True
            protocol.save()
            return Response('delete is success', status.HTTP_200_OK)
        except:
            traceback.print_exc()
            return Response(status.HTTP_400_BAD_REQUEST)
