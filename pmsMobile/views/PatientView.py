# oxit doctor view
import traceback

from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from pms.models.Patient import Patient
from pmsDoctor.serializers.PatientSerializer import PatientSerializer


class PatientProfileApi(APIView):
    def get(self, request, format=None):
        try:
            patient = Patient.objects.get(profile__user=request.user)
            api_data = dict()
            api_data['firstName'] = patient.profile.user.first_name
            api_data['lastName'] = patient.profile.user.last_name
            api_data['identityNumber'] = patient.profile.profileImage
            api_data['email'] = patient.profile.identityNumber
            api_data['address'] = patient.profile.address
            api_data['mobilePhone'] = patient.profile.mobilePhone
            api_data['birthDate'] = patient.birthDate
            api_gender_data = dict()
            api_gender_data['label'] = patient.gender.name
            api_gender_data['value'] = patient.gender.id
            api_data['gender'] = api_gender_data
            api_blood_data = dict()
            api_blood_data['label'] = patient.bloodGroup.name
            api_blood_data['value'] = patient.bloodGroup.id
            api_data['bloodGroup'] = api_blood_data

            serializer = PatientSerializer(api_data, context={'request': request})

            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            traceback.print_exc()
            return Response(str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
