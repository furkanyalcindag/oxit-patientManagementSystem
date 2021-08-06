# oxit staff view
import traceback

from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

from pms.models.MedicineDiagnosis import MedicineDiagnosis
from pmsDoctor.serializers.MedicineSerializer import MedicineSerializer


class MedicineDiagnosisApi(APIView):
    def get(self, request, format=None):
        try:
            if request.GET.get('id') is not None:
                medicineDiagnoses = MedicineDiagnosis.objects.filter(diagnosis__uuid=request.GET.get('id'))
                arr = []
                if medicineDiagnoses is not None:
                    for data in medicineDiagnoses:
                        api_object = dict()
                        api_object['id'] = data.medicine.id
                        api_object['name'] = data.medicine.name
                        arr.append(api_object)
                    serializer = MedicineSerializer(arr, many=True, context={'request': request})
                    return Response(serializer.data, status.HTTP_200_OK)
        except Exception as e:
            traceback.print_exc()
            return Response("", status.HTTP_500_INTERNAL_SERVER_ERROR)
