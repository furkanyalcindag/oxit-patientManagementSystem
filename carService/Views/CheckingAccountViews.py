from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from carService.models import CheckingAccount, PaymentMovement, PaymentType
from carService.models.ApiObject import APIObject
from carService.models.SelectObject import SelectObject
from carService.serializers.CheckingAccountSerializer import CheckingAccountPageSerializer, PaymentSerializer
from carService.serializers.GeneralSerializer import SelectSerializer


class CheckingAccountApi(APIView):
    # permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        checking_accounts = CheckingAccount.objects.all().order_by('-id')
        checking_account_array = []
        for checking_account in checking_accounts:
            data = dict()
            data['plate'] = checking_account.service.car.plate
            data['serviceDate'] = checking_account.service.creationDate.strftime("%d-%m-%Y %H:%M:%S")
            data['customerName'] = checking_account.service.car.profile.firmName \
                if checking_account.service.car.profile.isCorporate \
                else checking_account.service.car.profile.user.first_name + ' ' + checking_account.service.car.profile \
                .user.last_name
            data['totalPrice'] = checking_account.service.totalPrice
            data['remainingPrice'] = checking_account.remainingDebt
            data['paymentSituation'] = checking_account.paymentSituation.name
            checking_account_array.append(data)

        api_object = APIObject()
        api_object.data = checking_account_array
        api_object.recordsFiltered = checking_accounts.count()
        api_object.recordsTotal = checking_accounts.count()

        serializer = CheckingAccountPageSerializer(api_object, context={'request': request})
        return Response(serializer.data, status.HTTP_200_OK)


class PaymentAccountApi(APIView):
    # permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        checking_account = CheckingAccount.objects.get(uuid=request.GET.get('uuid'))
        payment_movements = PaymentMovement.objects.filter(checkingAccount=checking_account).order_by('-id')
        payment_movement_array = []
        for payment_movement in payment_movements:
            data = dict()
            data['paymentAmount'] = payment_movement.paymentAmount
            data['paymentDate'] = payment_movement.creationDate.strftime("%d-%m-%Y %H:%M:%S")
            data['paymentTypeDesc'] = payment_movement.paymentType.name
            data['checkingAccountUUID'] = payment_movement.uuid

            payment_movement_array.append(data)

        serializer = PaymentSerializer(payment_movement_array, context={'request': request})
        return Response(serializer.data, status.HTTP_200_OK)

    def post(self, request, format=None):
        serializer = PaymentSerializer(data=request.data, context={'request': request})

        if serializer.is_valid():
            serializer.save()
            return Response({"message": "payment is created"}, status=status.HTTP_200_OK)
        else:

            errors_dict = dict()
            for key, value in serializer.errors.items():
                if key == 'paymentAmount':
                    errors_dict['Ödeme Miktarı'] = value
                elif key == 'paymentType':
                    errors_dict['Ödeme Tipi'] = value

            return Response(errors_dict, status=status.HTTP_400_BAD_REQUEST)


class PaymentTypeSelectApi(APIView):
    #permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        types = PaymentType.objects.all()
        types_objects = []
        select_object_root = SelectObject()
        select_object_root.label = "Seçiniz"
        select_object_root.value = ""
        types_objects.append(select_object_root)

        for type in types:
            select_object = SelectObject()
            select_object.label = type.name
            select_object.value = type.id
            types_objects.append(select_object)

        serializer = SelectSerializer(types_objects, many=True, context={'request': request})
        return Response(serializer.data, status.HTTP_200_OK)
