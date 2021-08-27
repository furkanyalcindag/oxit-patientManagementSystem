import traceback

from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

from management.models.APIObject import APIObject
from management.serializers.CompanySerializer import CompanyPageableSerializer, CompanySerializer
from management.serializers.GeneralSerializer import SelectSerializer
from pms.models.Company import Company
from pms.models.SelectObject import SelectObject


class CompanyApi(APIView):
    def get(self, request, format=None):
        try:
            if request.GET.get('id') is not None:
                company = Company.objects.get(uuid=request.GET.get('id'))
                api_object = dict()
                api_object['uuid'] = company.uuid
                api_object['companyName'] = company.user.first_name
                api_object['email'] = company.user.email
                api_object['taxOffice'] = company.taxOffice
                api_object['taxNumber'] = company.taxNumber
                serializer = CompanySerializer(api_object, context={'request': request})
                return Response(serializer.data, status.HTTP_200_OK)

            else:
                active_page = 1
                count = 0
                name = ''
                if request.GET.get('activePage') is not None:
                    active_page = int(request.GET.get('activePage'))
                lim_start = 10 * (int(active_page) - 1)
                lim_end = lim_start + 10
                data = Company.objects.filter(user__first_name__icontains=name, isDeleted=False).order_by('-id')[
                       lim_start:lim_end]
                count = Company.objects.filter(isDeleted=False).count()
                arr = []
                for d in data:
                    api_object = dict()
                    api_object['uuid'] = d.uuid
                    api_object['companyName'] = d.user.first_name
                    api_object['email'] = d.user.email
                    api_object['taxOffice'] = d.taxOffice
                    api_object['taxNumber'] = d.taxNumber
                    arr.append(api_object)
                api_object = APIObject()
                api_object.data = arr
                api_object.recordsFiltered = data.count()
                api_object.recordsTotal = count
                if count % 10 == 0:
                    api_object.activePage = count / 10
                else:
                    api_object.activePage = (count / 10) + 1
                serializer = CompanyPageableSerializer(api_object, context={'request': request})
                return Response(serializer.data, status.HTTP_200_OK)
        except Exception as e:
            traceback.print_exc()
            return Response("", status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request, format=None):
        serializer = CompanySerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "company is created"}, status.HTTP_200_OK)
        else:
            errors = dict()
            for key, value in serializer.errors.items():
                if key == 'companyName':
                    errors['companyName'] = value
                elif key == 'email':
                    errors['email'] = value
                elif key == 'taxOffice':
                    errors['taxOffice'] = value
                elif key == 'taxNumber':
                    errors['taxNumber'] = value
            return Response(errors, status.HTTP_400_BAD_REQUEST)

    def put(self, request, format=None):
        try:
            instance = Company.objects.get(uuid=request.GET.get('id'))
            serializer = CompanySerializer(data=request.data, instance=instance, context={'request': request})

            if serializer.is_valid():
                serializer.save()
                return Response({'message': 'company is updated'}, status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            traceback.print_exc()
            return Response(status.HTTP_400_BAD_REQUEST)

    def delete(self, request, format=None):
        try:
            company = Company.objects.get(uuid=request.GET.get('id'))
            company.isDeleted = True
            company.save()
            return Response('delete is succes', status.HTTP_200_OK)
        except Exception as e:
            traceback.print_exc()
            return Response(status.HTTP_400_BAD_REQUEST)


class CompanySelectApi(APIView):
    def get(self, request, format=None):
        try:
            data = Company.objects.filter(isDeleted=False)
            arr = []
            for d in data:
                select_object = SelectObject()
                select_object.label = d.user.first_name
                select_object.value = d.id
                arr.append(select_object)
            serializer = SelectSerializer(arr, many=True, context={'request': request})
            return Response(serializer.data, status.HTTP_200_OK)
        except:
            return Response("error", status.HTTP_500_INTERNAL_SERVER_ERROR)
