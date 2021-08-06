# oxit staff view
import traceback

from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

from management.models.APIObject import APIObject
from pms.models.Diagnosis import Diagnosis
from pmsDoctor.serializers.DiagnosisSerializer import DiagnosisSerializer, DiagnosisPageableSerializer


class DiagnosisApi(APIView):
    def get(self, request, format=None):
        try:
            if request.GET.get('id') is not None:
                diagnosis = Diagnosis.objects.get(protocol_id=request.GET.get('id'))
                api_object = dict()
                api_object['uuid'] = diagnosis.uuid
                api_object['diagnosis'] = diagnosis.diagnosis
                serializer = DiagnosisSerializer(api_object, context={'request': request})
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

                data = Diagnosis.objects.filter(diagnosis__icontains=name, isDeleted=False).order_by('-id')[
                       lim_start:lim_end]
                filtered_count = Diagnosis.objects.filter(diagnosis__icontains=name, isDeleted=False).count()
                arr = []

                for diagnosis in data:
                    api_object = dict()
                    api_object['uuid'] = diagnosis.uuid
                    api_object['diagnosis'] = diagnosis.diagnosis
                    arr.append(api_object)
                api_object = APIObject()
                api_object.data = arr
                api_object.recordsFiltered = filtered_count
                api_object.recordsTotal = Diagnosis.objects.filter(isDeleted=False).count()
                serializer = DiagnosisPageableSerializer(api_object, context={'request': request})
                return Response(serializer.data, status.HTTP_200_OK)

        except Exception as e:
            traceback.print_exc()
            return Response("", status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request, format=None):
        serializer = DiagnosisSerializer(data=request.data, context={'request', request})
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "diagnosis is created"}, status=status.HTTP_200_OK)
        else:
            errors = dict()
            for key, value in serializer.errors.items():
                if key == 'diagnosis':
                    errors['diagnosis'] = value
                elif key == 'protocolId':
                    errors['protocolId'] = value
                elif key == 'medicines':
                    errors['medicines'] = value
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)
