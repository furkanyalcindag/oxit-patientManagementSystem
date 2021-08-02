# oxit doctor view
import traceback

from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from pmsDoctor.models.APIObject import APIObject
from pms.models.Patient import Patient
from pmsDoctor.serializers.PatientSerializer import PatientSerializer, PatientPageableSerializer


class PatientApi(APIView):
    def get(self, request, format=None):
        try:
            if request.GET.get('id') is not None:
                patient = Patient.objects.get(uuid=request.GET.get('id'))
                api_object = dict()
                api_object['uuid'] = patient.uuid
                api_object['firstName'] = patient.profile.user.first_name
                api_object['lastName'] = patient.profile.user.last_name
                api_object['email'] = patient.profile.user.email
                api_object['mobilePhone'] = patient.profile.mobilePhone
                api_object['identityNumber'] = patient.profile.identityNumber
                api_object['address'] = patient.profile.address
                api_object['birthDate'] = patient.birthDate
                api_gender_data = dict()
                api_gender_data['label'] = patient.gender.name
                api_gender_data['value'] = patient.gender.id
                api_object['gender'] = api_gender_data
                api_blood_data = dict()
                api_blood_data['label'] = patient.bloodGroup.name
                api_blood_data['value'] = patient.bloodGroup.id

                api_object['bloodGroup'] = api_blood_data

                serializer = PatientSerializer(api_object, context={'request': request})
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

                data = Patient.objects.filter(profile__user__first_name__icontains=name, profile__user__groups__id=10,
                                              isDeleted=False).order_by('-id')[lim_start:lim_end]
                filtered_count = Patient.objects.filter(profile__user__first_name__icontains=name,
                                                        profile__user__groups=10,
                                                        isDeleted=False).count()
                arr = []

                for patient in data:
                    api_object = dict()
                    api_object['uuid'] = patient.uuid
                    api_object['firstName'] = patient.profile.user.first_name
                    api_object['lastName'] = patient.profile.user.last_name
                    api_object['email'] = patient.profile.user.email
                    api_object['mobilePhone'] = patient.profile.mobilePhone
                    api_object['address'] = patient.profile.address
                    api_object['identityNumber'] = patient.profile.identityNumber
                    api_object['birthDate'] = patient.birthDate
                    api_gender_data = dict()
                    api_gender_data['label'] = patient.gender.name
                    api_gender_data['value'] = patient.gender.id
                    api_object['gender'] = api_gender_data
                    api_blood_data = dict()
                    api_blood_data['label'] = patient.bloodGroup.name
                    api_blood_data['value'] = patient.bloodGroup.id

                    api_object['bloodGroup'] = api_blood_data
                    arr.append(api_object)
                api_object = APIObject()
                api_object.data = arr
                api_object.recordsFiltered = filtered_count
                api_object.recordsTotal = Patient.objects.filter(isDeleted=False).count()
                serializer = PatientPageableSerializer(api_object, context={'request': request})
                return Response(serializer.data, status.HTTP_200_OK)

        except Exception as e:
            traceback.print_exc()
            return Response("", status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request, format=None):
        serializer = PatientSerializer(data=request.data, context={'request', request})
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "patient is created"}, status=status.HTTP_200_OK)
        else:
            errors = dict()
            for key, value in serializer.errors.items():
                if key == 'firstName':
                    errors['isim'] = value
                elif key == 'lastName':
                    errors['soyisim'] = value
                elif key == 'email':
                    errors['mail'] = value
                elif key == 'bloodGroupId':
                    errors['bloodGroupId'] = value
                elif key == 'genderId':
                    errors['genderId'] = value
                elif key == 'mobilePhone':
                    errors['mobilePhone'] = value
                elif key == 'address':
                    errors['address'] = value
                elif key == 'birthDate':
                    errors['birthDate'] = value
                elif key == 'identityNumber':
                    errors['identityNumber'] = value
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, format=None):
        try:
            instance = Patient.objects.get(uuid=request.GET.get('id'))
            serializer = PatientSerializer(data=request.data, instance=instance, context={'request': request})
            if serializer.is_valid():
                serializer.save()
                return Response({'message': "patient is updated"}, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception:
            traceback.print_exc()
            return Response(status.HTTP_400_BAD_REQUEST)

    def delete(self, request, format=None):
        try:
            patient = Patient.objects.get(uuid=request.GET.get('id'))
            patient.isDeleted = True
            patient.save()
            return Response('delete is success', status.HTTP_200_OK)
        except:
            traceback.print_exc()
            return Response(status.HTTP_400_BAD_REQUEST)