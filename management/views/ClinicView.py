import traceback

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from management.models.APIObject import APIObject
from management.serializers.ClinicSerializer import ClinicPageableSerializer, ClinicSerializer, \
    ClinicGeneralInfoSerializer, ClinicMediaSerializer
from pms.models import Clinic
from pms.models.ClinicMedia import ClinicMedia


class ClinicApi(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):

        try:

            if request.GET.get('id') is not None:

                clinic = Clinic.objects.get(uuid=request.GET.get('id'))

                api_object = dict()
                api_object['uuid'] = clinic.uuid
                api_object['clinicName'] = clinic.name
                api_object['taxOffice'] = clinic.taxOffice
                api_object['taxNumber'] = clinic.taxNumber
                api_object['address'] = clinic.address
                api_object['staffName'] = clinic.profile.user.first_name
                api_object['staffSurname'] = clinic.profile.user.last_name
                api_object['email'] = clinic.profile.user.email
                api_object['telephoneNumber'] = clinic.telephoneNumber

                api_city_data = dict()
                api_city_data['label'] = clinic.city.name
                api_city_data['value'] = clinic.city.id

                api_district_data = dict()
                api_district_data['label'] = clinic.district.name
                api_district_data['value'] = clinic.district.id

                api_object['city'] = api_city_data
                api_object['district'] = api_district_data

                serializer = ClinicSerializer(
                    api_object, context={'request': request})

                return Response(serializer.data, status.HTTP_200_OK)
            else:
                active_page = 1
                count = 0

                name = ''

                if request.GET.get('activePage') is not None:
                    active_page = int(request.GET.get('activePage'))

                lim_start = 10 * (int(active_page) - 1)
                lim_end = lim_start + 10

                data = Clinic.objects.filter(name__icontains=name, isDeleted=False).order_by('-id')[
                       lim_start:lim_end]

                count = Clinic.objects.filter(isDeleted=False).count()
                arr = []

                for clinic in data:
                    api_object = dict()
                    api_object['uuid'] = clinic.uuid
                    api_object['clinicName'] = clinic.name
                    api_object['taxOffice'] = clinic.taxOffice
                    api_object['taxNumber'] = clinic.taxNumber
                    api_object['address'] = clinic.address
                    api_object['cityDistrict'] = clinic.city.name + '/' + clinic.district.name
                    api_object['staffName'] = clinic.profile.user.first_name
                    api_object['staffSurname'] = clinic.profile.user.last_name
                    api_object['email'] = clinic.profile.user.email
                    api_object['telephoneNumber'] = clinic.telephoneNumber

                    api_city_data = dict()
                    api_city_data['label'] = clinic.city.name
                    api_city_data['value'] = clinic.city.id

                    api_district_data = dict()
                    api_district_data['label'] = clinic.district.name
                    api_district_data['value'] = clinic.district.id

                    api_object['city'] = api_city_data
                    api_object['district'] = api_district_data
                    arr.append(api_object)

                api_object = APIObject()
                api_object.data = arr
                api_object.recordsFiltered = data.count()
                api_object.recordsTotal = count
                if count % 10 == 0:
                    api_object.activePage = count / 10
                else:
                    api_object.activePage = (count / 10) + 1

                serializer = ClinicPageableSerializer(
                    api_object, context={'request': request})

                return Response(serializer.data, status.HTTP_200_OK)

        except Exception as e:
            traceback.print_exc()
            return Response("", status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request, format=None):
        serializer = ClinicSerializer(data=request.data, context={'request': request})

        if serializer.is_valid():
            serializer.save()
            return Response({"message": "clinic is created"}, status=status.HTTP_200_OK)
        else:
            errors = dict()
            for key, value in serializer.errors.items():
                if key == 'clinicName':
                    errors['Klinik Adı'] = value
                elif key == 'taxOffice':
                    errors['Vergi Dairesi'] = value
                elif key == 'taxNumber':
                    errors['Vergi No'] = value
                elif key == 'address':
                    errors['Adres'] = value
                elif key == 'cityId':
                    errors['İl'] = value
                elif key == 'districtId':
                    errors['İlçe'] = value
                elif key == 'mail':
                    errors['Mail'] = value
                elif key == 'staffName':
                    errors['Yetkili Ad'] = value
                elif key == 'staffSurname':
                    errors['Yetkili Soyadı'] = value
                elif key == 'telephoneNumber':
                    errors['Telefon Numarası'] = value

            return Response(errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, format=None):
        instance = Clinic.objects.get(uuid=request.GET.get('id'))
        serializer = ClinicSerializer(data=request.data, instance=instance, context={'request': request})

        if serializer.is_valid():
            serializer.save()
            return Response({'message': "Clinic is updated"}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, format=None):
        try:
            clinic = Clinic.objects.get(uuid=request.GET.get('id'))
            clinic.isDeleted = True
            clinic.save()
            return Response('delete is success', status.HTTP_200_OK)
        except:
            traceback.print_exc()
            return Response(status.HTTP_400_BAD_REQUEST)


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
