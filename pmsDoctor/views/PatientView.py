# oxit doctor view
import traceback

from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

from pms.models import Staff
from pms.models.PatientClinic import PatientClinic
from pms.models.SelectObject import SelectObject
from pmsDoctor.models.APIObject import APIObject
from pms.models.Patient import Patient
from pmsDoctor.serializers.GeneralSerializer import SelectSerializer
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
                count = 0

                name = ''
                if request.GET.get('activePage') is not None:
                    active_page = int(request.GET.get('activePage'))

                lim_start = 10 * (int(active_page) - 1)
                lim_end = lim_start + 10
                doctor = None

                if request.user.groups.values('name')[0]['name'] == 'Doctor':
                    doctor = Staff.objects.get(profile__user=request.user)
                    data = PatientClinic.objects.filter(clinic=doctor.clinic,
                                                        patient__profile__user__first_name__icontains=name,
                                                        patient__profile__user__groups__name='Patient',
                                                        patient__isDeleted=False).order_by('-id')[lim_start:lim_end]
                    count = PatientClinic.objects.filter(clinic=doctor.clinic, patient__isDeleted=False).count()
                else:
                    data = PatientClinic.objects.filter(clinic__profile__user=request.user,
                                                        patient__profile__user__first_name__icontains=name,
                                                        patient__profile__user__groups__name='Patient',
                                                        patient__isDeleted=False).order_by('-id')[lim_start:lim_end]
                    count = PatientClinic.objects.filter(clinic__profile__user=request.user,
                                                         patient__isDeleted=False).count()

                arr = []

                for patient in data:
                    api_object = dict()
                    api_object['uuid'] = patient.patient.uuid
                    api_object['firstName'] = patient.patient.profile.user.first_name
                    api_object['lastName'] = patient.patient.profile.user.last_name
                    api_object['email'] = patient.patient.profile.user.email
                    api_object['mobilePhone'] = patient.patient.profile.mobilePhone
                    api_object['address'] = patient.patient.profile.address
                    api_object['identityNumber'] = patient.patient.profile.identityNumber
                    api_object['birthDate'] = patient.patient.birthDate
                    api_gender_data = dict()
                    api_gender_data['label'] = patient.patient.gender.name
                    api_gender_data['value'] = patient.patient.gender.id
                    api_object['gender'] = api_gender_data
                    api_blood_data = dict()
                    api_blood_data['label'] = patient.patient.bloodGroup.name
                    api_blood_data['value'] = patient.patient.bloodGroup.id

                    api_object['bloodGroup'] = api_blood_data
                    arr.append(api_object)
                api_object = APIObject()
                api_object.data = arr
                api_object.recordsFiltered = data.count()
                api_object.recordsTotal = count
                if count % 10 == 0:
                    api_object.activePage = count / 10
                else:
                    api_object.activePage = (count / 10) + 1
                serializer = PatientPageableSerializer(api_object, context={'request': request})
                return Response(serializer.data, status.HTTP_200_OK)

        except Exception as e:
            traceback.print_exc()
            return Response("", status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request, format=None):
        serializer = PatientSerializer(data=request.data, context={'request': request})
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


class PatientSelectApi(APIView):
    def get(self, request, format=None):
        try:
            select_arr = []
            if request.user.groups.values('name')[0]['name'] == 'Doctor':
                doctor = Staff.objects.get(profile__user=request.user)
                data = PatientClinic.objects.filter(clinic=doctor.clinic,
                                                    patient__profile__user__groups__name='Patient',
                                                    patient__isDeleted=False).order_by('-id')

            else:
                data = PatientClinic.objects.filter(clinic__profile__user=request.user,
                                                    patient__profile__user__groups__name='Patient',
                                                    patient__isDeleted=False).order_by('-id')

            for patient in data:
                select_object = SelectObject()
                select_object.value = patient.patient.profile.user.id
                select_object.label = patient.patient.profile.user.first_name + ' ' + patient.patient.profile.user.last_name
                select_arr.append(select_object)

            serializer = SelectSerializer(select_arr, many=True, context={'request': request})

            return Response(serializer.data, status.HTTP_200_OK)
        except Exception as e:
            return Response("error", status.HTTP_500_INTERNAL_SERVER_ERROR)
