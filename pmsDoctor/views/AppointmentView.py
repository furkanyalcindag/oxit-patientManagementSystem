import traceback

from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

from pms.models import Appointment
from pmsDoctor.exceptions import AppointmentValidationException

from pmsDoctor.models.APIObject import APIObject
from pmsDoctor.serializers.AppointmentSerializer import AppointmentSerializer, AppointmentPageSerializer, \
    AppointmentCalendarSerializer

import datetime


class AppointmentApi(APIView):
    def get(self, request, format=None):
        try:
            if request.GET.get('id') is not None:
                appointment = Appointment.objects.get(uuid=request.GET.get('id'))
                api_object = dict()
                api_object['uuid'] = appointment.uuid
                api_object['date'] = appointment.date
                api_object['time'] = appointment.time
                api_object['endTime'] = appointment.endTime
                api_patient_data = dict()
                api_patient_data[
                    'label'] = appointment.patient.profile.user.first_name + ' ' + appointment.patient.profile.user.last_name
                api_patient_data['value'] = appointment.patient.profile.user.id
                api_object['patient'] = api_patient_data
                api_doctor_data = dict()
                api_doctor_data[
                    'label'] = appointment.doctor.profile.user.first_name + ' ' + appointment.doctor.profile.user.last_name
                api_doctor_data['value'] = appointment.doctor.profile.user.id
                api_object['doctor'] = api_doctor_data

                serializer = AppointmentSerializer(api_object, context={'request': request})
                return Response(serializer.data, status.HTTP_200_OK)

            else:
                active_page = 1
                count = 0

                name = ''
                if request.GET.get('activePage') is not None:
                    active_page = int(request.GET.get('activePage'))

                lim_start = 10 * (int(active_page) - 1)
                lim_end = lim_start + 10

                data = Appointment.objects.filter(doctor__profile__user=request.user,
                                                  patient__profile__user__first_name__icontains=name,
                                                  isDeleted=False).order_by('-id')[ lim_start:lim_end]
                count = Appointment.objects.filter(patient__profile__user__first_name__icontains=name,isDeleted=False).count()
                arr = []

                for appointment in data:
                    api_object = dict()
                    api_object['uuid'] = appointment.uuid
                    api_object['date'] = appointment.date
                    api_object['time'] = appointment.time
                    api_object['endTime'] = appointment.endTime
                    api_patient_data = dict()
                    api_patient_data[
                        'label'] = appointment.patient.profile.user.first_name + ' ' + appointment.patient.profile.user.last_name
                    api_patient_data['value'] = appointment.patient.profile.user.id
                    api_object['patient'] = api_patient_data
                    api_doctor_data = dict()
                    api_doctor_data[
                        'label'] = appointment.doctor.profile.user.first_name + ' ' + appointment.doctor.profile.user.last_name
                    api_doctor_data['value'] = appointment.doctor.profile.user.id
                    api_object['doctor'] = api_doctor_data
                    arr.append(api_object)
                api_object = APIObject()
                api_object.data = arr
                api_object.recordsFiltered = data.count()
                api_object.recordsTotal = count
                if count % 10 == 0:
                    api_object.activePage = count / 10
                else:
                    api_object.activePage = (count / 10) + 1
                serializer = AppointmentPageSerializer(api_object, context={'request': request})
                return Response(serializer.data, status.HTTP_200_OK)

        except Exception as e:
            traceback.print_exc()
            return Response("", status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request, format=None):
        try:
            serializer = AppointmentSerializer(data=request.data, context={'request': request})

            if datetime.datetime.strptime(request.data['date'], '%Y-%m-%d').date() < datetime.datetime.today().date():
                return Response({"message": "error"}, status=status.HTTP_417_EXPECTATION_FAILED)
            elif datetime.datetime.strptime(request.data['date'],
                                            '%Y-%m-%d').date() == datetime.datetime.today().date() and datetime.datetime.strptime(
                request.data['time'], '%H:%M').time() < datetime.datetime.today().time():
                return Response({"message": "error"}, status=status.HTTP_406_NOT_ACCEPTABLE)
            elif datetime.datetime.strptime(request.data['time'], '%H:%M').time() > datetime.datetime.strptime(
                    request.data['endTime'], '%H:%M').time():
                return Response({"message": "error"}, status=status.HTTP_301_MOVED_PERMANENTLY)
            elif serializer.is_valid():
                serializer.save()
                return Response({"message": "Appointment is created"}, status=status.HTTP_200_OK)
            elif datetime.datetime.strptime(request.data['date'],
                                            '%Y-%m-%d').date() == datetime.datetime.today().date() and datetime.datetime.strptime(
                request.data['time'], '%H:%M').time() < datetime.datetime.today().time():
                return Response({"message": "error"}, status=status.HTTP_406_NOT_ACCEPTABLE)
            else:
                errors = dict()
                for key, value in serializer.errors.items():
                    if key == 'patientId':
                        errors['patientId'] = value
                    elif key == 'doctorId':
                        errors['doctorId'] = value
                    elif key == 'date':
                        errors['date'] = value
                    elif key == 'time':
                        errors['time'] = value
                    elif key == 'endTime':
                        errors['endTime'] = value
                return Response(errors, status=status.HTTP_400_BAD_REQUEST)
        except AppointmentValidationException as e:
            return Response("", status=status.HTTP_406_NOT_ACCEPTABLE)
        except Exception as e:

            traceback.print_exc()

            if e.args[0] == 'Lütfen geçerli bir tarih ve zaman giriniz':
                return Response("", status=status.HTTP_406_NOT_ACCEPTABLE)

            else:
                return Response("", status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request, format=None):
        try:
            instance = Appointment.objects.get(uuid=request.GET.get('id'))
            serializer = AppointmentSerializer(data=request.data, instance=instance, context={'request': request})
            if datetime.datetime.strptime(request.data['date'], '%Y-%m-%d').date() < datetime.datetime.today().date():
                return Response({"message": "error"}, status=status.HTTP_417_EXPECTATION_FAILED)
            elif datetime.datetime.strptime(request.data['time'], '%H:%M').time() > datetime.datetime.strptime(
                    request.data['endTime'], '%H:%M').time():
                return Response({"message": "error"}, status=status.HTTP_301_MOVED_PERMANENTLY)
            elif datetime.datetime.strptime(request.data['date'],
                                            '%Y-%m-%d').date() == datetime.datetime.today().date() and datetime.datetime.strptime(
                request.data['time'], '%H:%M').time() < datetime.datetime.today().time():
                return Response({"message": "error"}, status=status.HTTP_406_NOT_ACCEPTABLE)
            elif datetime.datetime.strptime(request.data['date'],
                                            '%Y-%m-%d').date() == datetime.datetime.today().date() and datetime.datetime.strptime(
                request.data['endTime'], '%H:%M').time() < datetime.datetime.today().time():
                return Response({"message": "error"}, status=status.HTTP_304_NOT_MODIFIED)
            elif serializer.is_valid():
                serializer.save()
                return Response({"message": "Appointment is updated"}, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception:
            traceback.print_exc()
            return Response(status.HTTP_400_BAD_REQUEST)
        except AppointmentValidationException as e:
            return Response("", status=status.HTTP_406_NOT_ACCEPTABLE)
        except Exception as e:

            traceback.print_exc()

            if e.args[0] == 'Lütfen geçerli bir tarih ve zaman giriniz':
                return Response("", status=status.HTTP_406_NOT_ACCEPTABLE)

            else:
                return Response("", status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, format=None):
        try:
            appointment = Appointment.objects.get(uuid=request.GET.get('id'))
            appointment.isDeleted = True
            appointment.save()
            return Response('delete is success', status.HTTP_200_OK)
        except:
            traceback.print_exc()
            return Response(status.HTTP_400_BAD_REQUEST)


class AppointmentCalendarApi(APIView):
    def get(self, request, format=None):
        date = request.GET.get('date')

        if request.GET.get('id') is None:

            date_start = request.GET.get('startTime').split(' ')[0]
            date_end = request.GET.get('endTime').split(' ')[0]
            appointments = Appointment.objects.filter(date__gte=date_start, date__lte=date_end,
                                                      isDeleted=False)

            appointment_arr = []
            for appointment in appointments:
                api_object = dict()
                api_object['uuid'] = appointment.uuid
                api_object[
                    'title'] = appointment.patient.profile.user.first_name + ' ' + appointment.patient.profile.user.last_name
                api_object['start'] = str(appointment.date) + ' ' + str(appointment.time)
                api_object['end'] = str(appointment.date) + ' ' + str(appointment.endTime)
                api_object[
                    'doctorName'] = appointment.doctor.profile.user.first_name + ' ' + appointment.doctor.profile.user.last_name
                api_object['id'] = 'undone'

                appointment_arr.append(api_object)

            serializer = AppointmentCalendarSerializer(appointment_arr, many=True, context={'request': request})

            return Response(serializer.data, status.HTTP_200_OK)

        else:
            appointment = Appointment.objects.get(uuid=request.GET.get('id'))
            api_object = dict()
            api_object['uuid'] = appointment.uuid
            api_object['date'] = appointment.date
            api_object['time'] = appointment.time
            api_object['endTime'] = appointment.endTime

            select_doctor = dict()

            select_doctor[
                'label'] = appointment.doctor.profile.user.first_name + ' ' + appointment.doctor.profile.user.last_name
            select_doctor['value'] = appointment.doctor.profile.user.id
            select_patient = dict()

            select_patient[
                'label'] = appointment.patient.profile.user.first_name + ' ' + appointment.patient.profile.user.last_name
            select_patient['value'] = appointment.patient.profile.user.id

            api_object['doctor'] = select_doctor
            api_object['patient'] = select_patient
            serializer = AppointmentSerializer(api_object, context={'request': request})

            return Response(serializer.data, status.HTTP_200_OK)
