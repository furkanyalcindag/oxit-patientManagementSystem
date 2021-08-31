import traceback

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from management.serializers.ClinicSerializer import ClinicGeneralInfoSerializer, ClinicMediaSerializer
from pms.models import Clinic
from pms.models.ClinicMedia import ClinicMedia


class ClinicGeneralInfoApi(APIView):
    def get(self, request, format=None):
        try:
            clinic = Clinic.objects.get(profile__user=request.user)
            api_data = dict()
            api_data['clinicName'] = clinic.name
            api_data['staff'] = clinic.profile.user.first_name + ' ' + clinic.profile.user.last_name
            api_data['email'] = clinic.profile.user.email
            api_data['taxNumber'] = clinic.taxNumber
            api_data['taxOffice'] = clinic.taxOffice
            api_data['taxNumber'] = clinic.taxNumber
            api_data['address'] = clinic.address
            api_data['telephoneNumber'] = clinic.telephoneNumber
            api_data['district'] = clinic.district
            api_data['taxNumber'] = clinic.taxNumber
            api_city_data = dict()
            api_city_data['label'] = clinic.city.name
            api_city_data['value'] = clinic.city.id

            api_district_data = dict()
            api_district_data['label'] = clinic.district.name
            api_district_data['value'] = clinic.district.id

            api_data['city'] = api_city_data
            api_data['district'] = api_district_data
            serializer = ClinicGeneralInfoSerializer(
                api_data, context={'request': request})

            return Response(serializer.data, status.HTTP_200_OK)

        except:
            traceback.print_exc()
            return Response("", status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request, format=None):
        try:
            instance = Clinic.objects.get(profile__user=request.user)
            serializer = ClinicGeneralInfoSerializer(data=request.data, instance=instance,
                                                     context={'request': request})
            if serializer.is_valid():
                serializer.save()
                return Response({"message": "doctor information is updated"}, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except:
            traceback.print_exc()
            return Response('error', status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ClinicMediaApi(APIView):
    def get(self, request, format=None):
        try:
            clinicMedia = ClinicMedia.objects.get(clinic__profile__user_id=request.user.id)
            api_data = dict()
            api_data['uuid'] = clinicMedia.uuid
            api_data['media'] = clinicMedia.media
            serializer = ClinicMediaSerializer(
                api_data, context={'request': request})

            return Response(serializer.data, status.HTTP_200_OK)

        except:
            traceback.print_exc()
            return Response("", status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request, format=None):
        try:
            serializer = ClinicMediaSerializer(data=request.data,
                                               context={'request': request})
            if serializer.is_valid():
                serializer.save()
                return Response({"message": "clinic media is created"}, status=status.HTTP_200_OK)
            else:
                errors = dict()
                for key, value in serializer.errors.items():
                    if key == 'media':
                        errors['media'] = value
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except:
            traceback.print_exc()
            return Response('error', status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, format=None):
        try:
            media = ClinicMedia.objects.get(uuid=request.GET.get('id'),
                                            doctor__profile__user=request.user)
            media.isDeleted = True
            media.save()

            return Response(status=status.HTTP_200_OK)
        except Exception:
            traceback.print_exc()
            return Response(status=status.HTTP_400_BAD_REQUEST)
