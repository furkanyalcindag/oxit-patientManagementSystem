# oxit staff view
import traceback

from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

from management.models.APIObject import APIObject
from pms.models import Profile
from pms.models.AssayResult import AssayResult
from pmsDoctor.serializers.AssayResultSerializer import AssayResultSerializer
from pmsDoctor.serializers.SecretarySerializer import SecretarySerializer, SecretaryPageableSerializer


class AssayResultApi(APIView):
    def get(self, request, format=None):
        try:
            result = AssayResult.objects.get(assay__uuid=request.GET.get('id'),
                                             patient__uuid=request.GET.get('patientId'))
            api_object = dict()
            api_object['uuid'] = result.uuid
            api_object['result'] = result.user.last_name
            api_assay_data = dict()
            api_assay_data['label'] = result.assay.name
            api_assay_data['value'] = result.assay.uuid
            api_object['assay'] = api_assay_data

            serializer = AssayResultSerializer(api_object, context={'request': request})
            return Response(serializer.data, status.HTTP_200_OK)

        except Exception as e:
            traceback.print_exc()
            return Response("", status.HTTP_500_INTERNAL_SERVER_ERROR)
