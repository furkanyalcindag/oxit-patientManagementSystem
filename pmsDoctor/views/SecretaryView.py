import traceback

from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

from management.models.APIObject import APIObject
from pms.models import Profile
from pmsDoctor.serializers.SecretarySerializer import SecretarySerializer, SecretaryPageableSerializer


class SecretaryApi(APIView):
    def get(self, request, format=None):
        try:
            if request.GET.get('id') is not None:
                secretary = Profile.objects.get(uuid=request.GET.get('id'))
                api_object = dict()
                api_object['uuid'] = secretary.uuid
                api_object['firstName'] = secretary.user.first_name
                api_object['lastName'] = secretary.user.last_name
                api_object['email'] = secretary.user.email
                api_group_data = dict()

                api_object['group'] = api_group_data

                serializer = SecretarySerializer(api_object, context={'request': request})
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

                data = Profile.objects.filter(user__first_name__icontains=name, user__groups__name='Secretary',
                                              isDeleted=False).order_by('-id')[
                       lim_start:lim_end]
                filtered_count = Profile.objects.filter(user__first_name__icontains=name,
                                                        user__groups__name='Secretary',
                                                        isDeleted=False).count()
                arr = []

                for secretary in data:
                    api_object = dict()
                    api_object['uuid'] = secretary.uuid
                    api_object['firstName'] = secretary.user.first_name
                    api_object['lastName'] = secretary.user.last_name
                    api_object['email'] = secretary.user.email
                    arr.append(api_object)
                api_object = APIObject()
                api_object.data = arr
                api_object.recordsFiltered = filtered_count
                api_object.recordsTotal = Profile.objects.filter(isDeleted=False,
                                                                 user__groups__name='Secretary').count()
                serializer = SecretaryPageableSerializer(api_object, context={'request': request})
                return Response(serializer.data, status.HTTP_200_OK)

        except Exception as e:
            traceback.print_exc()
            return Response("", status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request, format=None):
        serializer = SecretarySerializer(data=request.data, context={'request', request})
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Secretary is created"}, status=status.HTTP_200_OK)
        else:
            errors = dict()
            for key, value in serializer.errors.items():
                if key == 'firstName':
                    errors['isim'] = value
                elif key == 'lastName':
                    errors['soyisim'] = value
                elif key == 'email':
                    errors['mail'] = value
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, format=None):
        try:
            instance = Profile.objects.get(uuid=request.GET.get('id'))
            serializer = SecretarySerializer(data=request.data, instance=instance, context={'request': request})
            if serializer.is_valid():
                serializer.save()
                return Response({'message': "secretary is updated"}, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception:
            traceback.print_exc()
            return Response(status.HTTP_400_BAD_REQUEST)

    def delete(self, request, format=None):
        try:
            secretary = Profile.objects.get(uuid=request.GET.get('id'))
            secretary.isDeleted = True
            secretary.save()
            return Response('delete is success', status.HTTP_200_OK)
        except:
            traceback.print_exc()
            return Response(status.HTTP_400_BAD_REQUEST)
