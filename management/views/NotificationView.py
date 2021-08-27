from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

from management.serializers.NotificationSerializer import NotificationSerializer, NotificationPageSerializer
from pms.models import Notification
from pmsDoctor.models.APIObject import APIObject


class NotificationApi(APIView):

    def post(self, request, format=None):
        serializer = NotificationSerializer(data=request.data, context={'request': request})

        if serializer.is_valid():
            serializer.save()
            return Response({"message": "notification is created"}, status=status.HTTP_200_OK)
        else:
            errors = dict()
            for key, value in serializer.errors.items():
                if key == 'title':
                    errors['Baslik'] = value
                elif key == 'Image':
                    errors['fotograf'] = value
                elif key == 'body':
                    errors['Aciklama'] = value
                elif key == 'link':
                    errors['Link'] = value

            return Response(errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, format=None):
        active_page = 1
        count = 0
        if request.GET.get('activePage') is not None:
            active_page = int(request.GET.get('activePage'))
        lim_start = 10 * (int(active_page) - 1)
        lim_end = lim_start + 10
        notifications = Notification.objects.all().order_by('-id')[
                        lim_start:lim_end]
        count = Notification.objects.all().count()
        arr = []
        for notification in notifications:
            api_object = dict()
            api_object['uuid'] = notification.uuid
            api_object['title'] = notification.title
            api_object['body'] = notification.body
            api_object['image'] = notification.image
            api_object['link'] = notification.link
            arr.append(api_object)
        api_object = APIObject()
        api_object.data = arr
        api_object.recordsFiltered = notifications.count()
        api_object.recordsTotal = count
        if count % 10 == 0:
            api_object.activePage = count / 10
        else:
            api_object.activePage = (count / 10) + 1
        serializer = NotificationPageSerializer(api_object, context={'request': request})
        return Response(serializer.data, status.HTTP_200_OK)
