# oxit staff view
import traceback

from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

from management.models.APIObject import APIObject
from management.serializers.StaffSerializer import StaffSerializer, StaffPageableSerializer
from pms.models import Profile


class StaffApi(APIView):
    def get(self, request, format=None):
        try:
            if request.GET.get('id') is not None:
                staff = Profile.objects.get(uuid=request.GET.get('id'))
                api_object = dict()
                api_object['uuid'] = staff.uuid
                api_object['firstName'] = staff.user.first_name
                api_object['lastName'] = staff.user.last_name
                api_object['mobilePhone'] = staff.mobilePhone
                api_object['address'] = staff.address
                api_object['email'] = staff.user.email
                api_group_data = dict()
                api_group_data['label'] = staff.user.groups.filter()[0].name
                api_group_data['value'] = staff.user.groups.filter()[0].id

                api_object['group'] = api_group_data

                serializer = StaffSerializer(api_object, context={'request': request})
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

                data = Profile.objects.filter(user__first_name__icontains=name, isDeleted=False).order_by('-id')[
                       lim_start:lim_end]
                filtered_count = Profile.objects.filter(user__first_name__icontains=name, isDeleted=False).count()
                arr = []

                for staff in data:
                    api_object = dict()
                    api_object['uuid'] = staff.uuid
                    api_object['firstName'] = staff.user.first_name
                    api_object['lastName'] = staff.user.last_name
                    api_object['mobilePhone'] = staff.mobilePhone
                    api_object['address'] = staff.address
                    api_object['email'] = staff.user.email
                    api_group_data = dict()
                    api_group_data['label'] = staff.user.groups.filter()[0].name
                    api_group_data['value'] = staff.user.groups.filter()[0].id
                    api_object['group'] = api_group_data
                    arr.append(api_object)
                api_object = APIObject()
                api_object.data = arr
                api_object.recordsFiltered = filtered_count
                api_object.recordsTotal = Profile.objects.filter(isDeleted=False).count()
                serializer = StaffPageableSerializer(api_object, context={'request': request})
                return Response(serializer.data, status.HTTP_200_OK)

        except Exception as e:
            traceback.print_exc()
            return Response("", status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request, format=None):
        serializer = StaffSerializer(data=request.data, context={'request', request})
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Staff is created"}, status=status.HTTP_200_OK)
        else:
            errors = dict()
            for key, value in serializer.errors.items():
                if key == 'firstName':
                    errors['isim'] = value
                elif key == 'lastName':
                    errors['soyisim'] = value
                elif key == 'email':
                    errors['mail'] = value
                elif key == 'groupId':
                    errors['group'] = value
                elif key == 'address':
                    errors['address'] = value
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, format=None):
        try:
            instance = Profile.objects.get(uuid=request.GET.get('id'))
            serializer = StaffSerializer(data=request.data, instance=instance, context={'request': request})
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
            staff = Profile.objects.get(uuid=request.GET.get('id'))
            staff.isDeleted = True
            staff.save()
            return Response('delete is success', status.HTTP_200_OK)
        except:
            traceback.print_exc()
            return Response(status.HTTP_400_BAD_REQUEST)
