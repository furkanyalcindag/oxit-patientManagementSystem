# oxit doctor view
import traceback

from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

from management.serializers.GeneralSerializer import SelectSerializer
from pms.models.SelectObject import SelectObject
from pmsDoctor.models.APIObject import APIObject
from pmsDoctor.serializers.DoctorSerializer import DoctorPageSerializer, DoctorSerializer
from pms.models.Staff import Staff


class DoctorApi(APIView):
    def get(self, request, format=None):
        try:
            if request.GET.get('id') is not None:
                staff = Staff.objects.get(uuid=request.GET.get('id'))
                api_object = dict()
                api_object['uuid'] = staff.uuid
                api_object['firstName'] = staff.profile.user.first_name
                api_object['lastName'] = staff.profile.user.last_name
                api_object['email'] = staff.profile.user.email
                api_object['diplomaNo'] = staff.diplomaNo
                api_object['insuranceNumber'] = staff.insuranceNumber
                api_object['title'] = staff.title
                api_department_data = dict()
                api_department_data['label'] = staff.department.name
                api_department_data['value'] = staff.department.id

                api_object['department'] = api_department_data

                serializer = DoctorSerializer(api_object, context={'request': request})
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

                data = Staff.objects.filter(profile__user__first_name__icontains=name, isDeleted=False).order_by('-id')[
                       lim_start:lim_end]
                filtered_count = Staff.objects.filter(profile__user__first_name__icontains=name,
                                                      isDeleted=False).count()
                arr = []

                for staff in data:
                    api_object = dict()
                    api_object['uuid'] = staff.uuid
                    api_object['firstName'] = staff.profile.user.first_name
                    api_object['lastName'] = staff.profile.user.last_name
                    api_object['diplomaNo'] = staff.diplomaNo
                    api_object['insuranceNumber'] = staff.insuranceNumber
                    api_object['title'] = staff.title
                    api_object['email'] = staff.profile.user.email
                    api_department_data = dict()
                    api_department_data['label'] = staff.department.name
                    api_department_data['value'] = staff.department.id
                    api_object['department'] = api_department_data
                    arr.append(api_object)
                api_object = APIObject()
                api_object.data = arr
                api_object.recordsFiltered = filtered_count
                api_object.recordsTotal = Staff.objects.filter(isDeleted=False).count()
                serializer = DoctorPageSerializer(api_object, context={'request': request})
                return Response(serializer.data, status.HTTP_200_OK)

        except Exception as e:
            traceback.print_exc()
            return Response("", status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request, format=None):
        serializer = DoctorSerializer(data=request.data, context={'request', request})
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Doctor is created"}, status=status.HTTP_200_OK)
        else:
            errors = dict()
            for key, value in serializer.errors.items():
                if key == 'firstName':
                    errors['isim'] = value
                elif key == 'lastName':
                    errors['soyisim'] = value
                elif key == 'email':
                    errors['mail'] = value
                elif key == 'departmentId':
                    errors['departmentId'] = value
                elif key == 'insuranceNumber':
                    errors['insuranceNumber'] = value
                elif key == 'diplomaNo':
                    errors['diplomaNo'] = value
                elif key == 'title':
                    errors['title'] = value
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, format=None):
        try:
            instance = Staff.objects.get(uuid=request.GET.get('id'))
            serializer = DoctorSerializer(data=request.data, instance=instance, context={'request': request})
            if serializer.is_valid():
                serializer.save()
                return Response({'message': "staff is updated"}, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception:
            traceback.print_exc()
            return Response(status.HTTP_400_BAD_REQUEST)

    def delete(self, request, format=None):
        try:
            staff = Staff.objects.get(uuid=request.GET.get('id'))
            staff.isDeleted = True
            staff.save()
            return Response('delete is success', status.HTTP_200_OK)
        except:
            traceback.print_exc()
            return Response(status.HTTP_400_BAD_REQUEST)


class DoctorSelectApi(APIView):
    def get(self, request, format=None):
        try:
            select_arr = []
            data = Staff.objects.all()

            for doctor in data:
                select_object = SelectObject()
                select_object.value = doctor.profile.user.id
                select_object.label = doctor.profile.user.first_name + ' ' + doctor.profile.user.last_name
                select_arr.append(select_object)

            serializer = SelectSerializer(select_arr, many=True, context={'request': request})

            return Response(serializer.data, status.HTTP_200_OK)
        except Exception as e:
            return Response("error", status.HTTP_500_INTERNAL_SERVER_ERROR)
