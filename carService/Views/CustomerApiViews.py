from django.db.models import Q
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from carService.models import Profile
from carService.models.ApiObject import APIObject
from carService.serializers.UserSerializer import CustomerAddSerializer, CustomerPageSerializer


class CustomerApi(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):

        search = request.GET.get('search')

        per_page = request.GET.get('per_page')
        page = request.GET.get('page')
        page = int(page) - 1
        start = (int(page) * int(per_page))
        end = start + int(per_page)

        data = Profile.objects.filter(user__groups__name__iexact='Customer').filter(
            Q(user__first_name__icontains=search) | Q(user__last_name__icontains=search) |
            Q(firmName__icontains=search)).order_by('-id')[start:end]

        apiObject = APIObject()
        apiObject.data = data
        apiObject.recordsFiltered = data.count()
        apiObject.recordsTotal = Profile.objects.filter(user__groups__name__iexact='Customer').count()

        serializer = CustomerPageSerializer(apiObject, context={'request': request})
        return Response(serializer.data, status.HTTP_200_OK)

    def post(self, request, format=None):
        serializer = CustomerAddSerializer(data=request.data, context={'request': request})

        if serializer.is_valid():
            serializer.save()
            return Response({"message": "user is created"}, status=status.HTTP_200_OK)
        else:
            errors_dict = dict()
            for key, value in serializer.errors.items():
                if key == 'group':
                    errors_dict['Grup'] = value
                elif key == 'username':
                    errors_dict['Email'] = value
                elif key == 'firstName':
                    errors_dict['İsim'] = value
                elif key == 'lastName':
                    errors_dict['Soyisim'] = value
                elif key == 'firmName':
                    errors_dict['Firma Adı'] = value
                elif key == 'taxNumber':
                    errors_dict['Vergi Numarası'] = value
                elif key == 'taxOffice':
                    errors_dict['Vergi Dairesi'] = value

            return Response(errors_dict, status=status.HTTP_400_BAD_REQUEST)
