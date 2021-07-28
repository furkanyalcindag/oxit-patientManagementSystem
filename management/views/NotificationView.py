from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

from management.serializers.NotificationSerializer import NotificationSerializer
from pms.models import Notification


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
        notifications = Notification.objects.all()
        serializer = NotificationSerializer(notifications, many=True, context={'request': request})
        return Response(serializer.data, status.HTTP_200_OK)