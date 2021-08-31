# oxit staff view
import traceback

from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

from management.models.APIObject import APIObject
from pms.models.Protocol import Protocol
from pmsDoctor.serializers.ProtocolSerializer import ProtocolSerializer, ProtocolPageableSerializer


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
