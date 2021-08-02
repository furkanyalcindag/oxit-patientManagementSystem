from rest_framework import status
from rest_framework.views import APIView

from pmsDoctor.serializers.GeneralSerializer import SelectSerializer
from pms.models.BloodGroup import BloodGroup
from pms.models.SelectObject import SelectObject
from rest_framework.response import Response


class BloodGroupSelectApi(APIView):
    def get(self, request, format=None):
        try:
            select_arr = []
            data = BloodGroup.objects.all()

            for group in data:
                select_object = SelectObject()
                select_object.value = group.id
                select_object.label = group.name
                select_arr.append(select_object)

            serializer = SelectSerializer(select_arr, many=True, context={'request': request})

            return Response(serializer.data, status.HTTP_200_OK)
        except Exception as e:
            return Response("error", status.HTTP_500_INTERNAL_SERVER_ERROR)
