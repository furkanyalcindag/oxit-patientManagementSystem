import traceback
import datetime
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

from management.models.APIObject import APIObject
from management.serializers.CompanyAdvertisingSerializer import CompanyAdvertisingSerializer, \
    CompanyAdvertisingPageableSerializer
from pms.models.CompanyAdvertising import CompanyAdvertising


class CompanyAdvertisingApi(APIView):
    def get(self, request, format=None):
        try:
            if request.GET.get('id') is not None:
                advertising = CompanyAdvertising.objects.get(uuid=request.GET.get('id'))
                api_object = dict()
                api_object['uuid'] = advertising.uuid
                api_object['name'] = advertising.name
                api_object['company'] = advertising.company.name
                api_object['location'] = advertising.ad.name
                api_object['publishEndDate'] = advertising.publishEndDate
                api_object['publishStartDate'] = advertising.publishStartDate
                api_object['price'] = advertising.price
                api_company_data = dict()
                api_company_data['label'] = advertising.company.user.first_name
                api_company_data['value'] = advertising.company.id
                api_location_data = dict()
                api_location_data['label'] = advertising.ad.name
                api_location_data['value'] = advertising.ad.id
                api_object['company'] = api_company_data
                api_object['location'] = api_location_data
                serializer = CompanyAdvertisingSerializer(api_object, context={'request': request})
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
                data = CompanyAdvertising.objects.filter(name__icontains=name, isDeleted=False).order_by(
                    '-id')[
                       lim_start:lim_end]
                filtered_count = CompanyAdvertising.objects.filter(name__icontains=name,
                                                                   isDeleted=False).count()
                arr = []
                for d in data:
                    api_object = dict()
                    api_object['uuid'] = d.uuid
                    api_object['name'] = d.name
                    api_object['publishEndDate'] = d.publishEndDate
                    api_object['publishStartDate'] = d.publishStartDate
                    api_object['price'] = d.price
                    api_company_data = dict()
                    api_company_data['label'] = d.company.user.first_name
                    api_company_data['value'] = d.company.id
                    api_location_data = dict()
                    api_location_data['label'] = d.ad.name
                    api_location_data['value'] = d.ad.id
                    api_object['company'] = api_company_data
                    api_object['location'] = api_location_data
                    arr.append(api_object)
                api_object = APIObject()
                api_object.data = arr
                api_object.recordsFiltered = filtered_count
                api_object.recordsTotal = CompanyAdvertising.objects.filter(isDeleted=False).count()
                serializer = CompanyAdvertisingPageableSerializer(api_object, context={'request': request})
                return Response(serializer.data, status.HTTP_200_OK)
        except Exception as e:
            traceback.print_exc()
            return Response("", status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request, format=None):
        serializer = CompanyAdvertisingSerializer(data=request.data, context={'request': request})
        if datetime.datetime.strptime(request.data['publishEndDate'],
                                      '%Y-%m-%d').date() < datetime.datetime.today().date():
            return Response({"message": "error"}, status=status.HTTP_417_EXPECTATION_FAILED)
        elif datetime.datetime.strptime(request.data['publishStartDate'],
                                        '%Y-%m-%d').date() < datetime.datetime.today().date():
            return Response({"message": "error"}, status=status.HTTP_301_MOVED_PERMANENTLY)
        elif datetime.datetime.strptime(request.data['publishStartDate'],
                                        '%Y-%m-%d').date() > datetime.datetime.strptime(request.data['publishEndDate'],
                                                                                        '%Y-%m-%d').date():
            return Response({"message": "error"}, status=status.HTTP_406_NOT_ACCEPTABLE)
        elif serializer.is_valid():
            serializer.save()
            return Response({"message": "advertising is created"}, status.HTTP_200_OK)
        else:
            errors = dict()
            for key, value in serializer.errors.items():
                if key == 'name':
                    errors['name'] = value
                elif key == 'companyId':
                    errors['companyId'] = value
                elif key == 'locationId':
                    errors['locationId'] = value
                elif key == 'publishEndDate':
                    errors['publishEndDate'] = value
                elif key == 'publishStartDate':
                    errors['publishStartDate'] = value
                elif key == 'price':
                    errors['price'] = value
            return Response(errors, status.HTTP_400_BAD_REQUEST)

    def put(self, request, format=None):
        try:
            instance = CompanyAdvertising.objects.get(uuid=request.GET.get('id'))
            serializer = CompanyAdvertisingSerializer(data=request.data, instance=instance,
                                                      context={'request', request})

            if datetime.datetime.strptime(request.data['publishEndDate'],
                                          '%Y-%m-%d').date() < datetime.datetime.today().date():
                return Response({"message": "error"}, status=status.HTTP_417_EXPECTATION_FAILED)
            elif datetime.datetime.strptime(request.data['publishStartDate'],
                                            '%Y-%m-%d').date() < datetime.datetime.today().date():
                return Response({"message": "error"}, status=status.HTTP_301_MOVED_PERMANENTLY)
            elif datetime.datetime.strptime(request.data['publishStartDate'],
                                            '%Y-%m-%d').date() > datetime.datetime.strptime(
                request.data['publishEndDate'], '%Y-%m-%d').date():
                return Response({"message": "error"}, status=status.HTTP_406_NOT_ACCEPTABLE)
            elif serializer.is_valid():
                serializer.save()
                return Response({'message': 'company is updated'}, status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            traceback.print_exc()
            return Response(status.HTTP_400_BAD_REQUEST)

    def delete(self, request, format=None):
        try:
            company = CompanyAdvertising.objects.get(uuid=request.GET.get('id'))
            company.isDeleted = True
            company.save()
            return Response('delete is succes', status.HTTP_200_OK)
        except Exception as e:
            traceback.print_exc()
            return Response(status.HTTP_400_BAD_REQUEST)
