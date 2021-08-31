# oxit staff view
import traceback

from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

from management.models.APIObject import APIObject
from pms.models.Protocol import Protocol
from pmsDoctor.serializers.ProtocolSerializer import ProtocolSerializer, ProtocolPageableSerializer


class ProtocolApi(APIView):
    def get(self, request, format=None):
        try:
            if request.GET.get('id') is not None:
                protocols = Protocol.objects.filter(patient__uuid=request.GET.get('id'), isDeleted=False)
                # patientın protokolleri
                arr = []
                for data in protocols:
                    api_object = dict()
                    api_object['uuid'] = data.uuid
                    api_object['description'] = data.description
                    api_object['situation'] = data.situation.name
                    api_object['price'] = data.price
                    api_patient_data = dict()
                    api_patient_data['label'] = data.patient.profile.user.first_name
                    api_patient_data['value'] = data.patient.id
                    api_object['patient'] = api_patient_data
                    arr.append(api_object)
                serializer = ProtocolSerializer(arr, many=True, context={'request': request})
                return Response(serializer.data, status.HTTP_200_OK)
            # patientın tek protokolü
            elif request.GET.get('protocolId') is not None:
                protocol = Protocol.objects.get(uuid=request.GET.get('protocolId'))
                api_object = dict()
                api_object['uuid'] = protocol.uuid
                api_object['description'] = protocol.description
                api_object['price'] = protocol.price
                api_object['protocolId'] = protocol.id
                api_object['situation'] = protocol.situation.name
                api_patient_data = dict()
                api_patient_data['label'] = protocol.patient.profile.user.first_name
                api_patient_data['value'] = protocol.patient.id
                api_object['patient'] = api_patient_data
                serializer = ProtocolSerializer(api_object, context={'request': request})
                return Response(serializer.data, status.HTTP_200_OK)

            else:
                # tüm protokoller
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
                    api_object['price'] = protocol.price
                    api_object['situation'] = protocol.situation.name
                    api_object['assay'] = protocol.description
                    api_patient_data = dict()
                    api_patient_data['label'] = protocol.patient.profile.user.first_name
                    api_patient_data['value'] = protocol.patient.id
                    api_object['patient'] = api_patient_data
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
            return Response({"message": "Protocol is created"}, status=status.HTTP_200_OK)
        else:
            errors = dict()
            for key, value in serializer.errors.items():
                if key == 'description':
                    errors['description'] = value
                elif key == 'patientId':
                    errors['patientId'] = value
                elif key == 'price':
                    errors['price'] = value
                # elif key == 'assays':
                #     errors['assays'] = value
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, format=None):
        try:
            instance = Protocol.objects.get(uuid=request.GET.get('id'))
            serializer = ProtocolSerializer(data=request.data, instance=instance, context={'request': request})
            if serializer.is_valid():
                serializer.save()
                return Response({'message': "protocol is updated"}, status=status.HTTP_200_OK)
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


class PatientProtocolApi(APIView):
    def get(self, request, format=None):
        try:
            # patientın tek protokolü
            if request.GET.get('protocolId') is not None:
                protocol = Protocol.objects.get(uuid=request.GET.get('protocolId'))
                api_object = dict()
                api_object['uuid'] = protocol.uuid
                api_object['description'] = protocol.description
                api_object['price'] = protocol.price
                api_object['protocolId'] = protocol.id
                api_object['situation'] = protocol.situation.name
                api_patient_data = dict()
                api_patient_data['label'] = protocol.patient.profile.user.first_name
                api_patient_data['value'] = protocol.patient.id
                api_object['patient'] = api_patient_data
                serializer = ProtocolSerializer(api_object, context={'request': request})
                return Response(serializer.data, status.HTTP_200_OK)
            else:
                active_page = 1
                count = 0
                if request.GET.get('activePage') is not None:
                    active_page = int(request.GET.get('activePage'))

                lim_start = 10 * (int(active_page) - 1)
                lim_end = lim_start + 10
                protocols = Protocol.objects.filter(patient__profile__user=request.user, isDeleted=False).order_by(
                    '-id')[
                            lim_start:lim_end]
                count = Protocol.objects.filter(patient__profile__user=request.user, isDeleted=False).count()
                # patientın protokolleri
                arr = []
                for data in protocols:
                    api_object = dict()
                    api_object['uuid'] = data.uuid
                    api_object['description'] = data.description
                    api_object['situation'] = data.situation.name
                    api_object['price'] = data.price
                    api_patient_data = dict()
                    api_patient_data['label'] = data.patient.profile.user.first_name
                    api_patient_data['value'] = data.patient.id
                    api_object['patient'] = api_patient_data
                    arr.append(api_object)
                api_object = APIObject()
                api_object.data = arr
                api_object.recordsFiltered = protocols.count()
                api_object.recordsTotal = count
                if count % 10 == 0:
                    api_object.activePage = count / 10
                else:
                    api_object.activePage = (count / 10) + 1
                serializer = ProtocolPageableSerializer(api_object, context={'request': request})
                return Response(serializer.data, status.HTTP_200_OK)
        except Exception as e:
            traceback.print_exc()
            return Response("", status.HTTP_500_INTERNAL_SERVER_ERROR)
