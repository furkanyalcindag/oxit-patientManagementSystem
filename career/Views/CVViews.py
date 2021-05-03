from rest_framework import status
from rest_framework.views import APIView

from career.models import Student, StudentEducationInfo
from career.serializers.CVSerializer import StudentEducationInfoSerializer
from rest_framework.response import Response


class StudentEducationInfoApi(APIView):

    def get(self, request, format=None):
        student = Student.objects.get(uuid=request.GET.get('uuid'))
        student_education_infos = StudentEducationInfo.objects.filter(student=student)
        serializer = StudentEducationInfoSerializer(student_education_infos, context={'request': request})
        return Response(serializer, status.HTTP_200_OK)

    def post(self, request, format=None):
        serializer = StudentEducationInfoSerializer(
            data=request.data, context={'request': request})

        if serializer.is_valid():
            serializer.save()
            return Response({"message": "service is created"}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
