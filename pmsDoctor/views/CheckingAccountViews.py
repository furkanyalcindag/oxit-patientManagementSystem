# oxit doctor view
import traceback

from django.db.models import Sum
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

from pms.models import PaymentType, CheckingAccount, PaymentMovement
from pms.models.SelectObject import SelectObject
from pmsDoctor.models.APIObject import APIObject
from pms.models.Patient import Patient
from pmsDoctor.serializers.CheckingAccountSerializer import PaymentSerializer, PaymentDiscountSerializer, \
    CheckingAccountSerializer, CheckingAccountPageSerializer, PaymentMovementPageSerializer
from pmsDoctor.serializers.GeneralSerializer import SelectSerializer
from pmsDoctor.serializers.PatientSerializer import PatientSerializer, PatientPageableSerializer


class PaymentAccountApi(APIView):
    def get(self, request, format=None):
        try:
            checking_account = CheckingAccount.objects.get(
                uuid=request.GET.get('id'))  # checking account uuid bekleniyor
            payment_movements = PaymentMovement.objects.filter(checkingAccount=checking_account).order_by('-id')
            payment_movement_array = []
            for payment_movement in payment_movements:
                data = dict()
                data['paymentAmount'] = payment_movement.paymentAmount
                data['paymentDate'] = payment_movement.creationDate.strftime("%d-%m-%Y %h:%M:%S")
                data['paymentTypeDesc'] = payment_movement.paymentType.name
                payment_movement_array.append(data)
            serializer = PaymentSerializer(payment_movement_array, many=True, context={'request': request})
            return Response(serializer.data, status.HTTP_200_OK)

        except Exception as e:
            traceback.print_exc()
            return Response("", status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request, format=None):
        serializer = PaymentSerializer(data=request.data, context={'request', request})
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "payment is created"}, status=status.HTTP_200_OK)
        else:
            errors = dict()
            for key, value in serializer.errors.items():
                if key == 'paymentAmount':
                    errors['paymentAmount'] = value
                elif key == 'paymentType':
                    errors['paymentType'] = value
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)


class PaymentAccountDiscountApi(APIView):
    def post(self, request, format=None):
        serializer = PaymentDiscountSerializer(data=request.data, context={'request': request})

        if serializer.is_valid():
            serializer.save()
            return Response({"message": "discount is created"}, status=status.HTTP_200_OK)
        else:

            errors_dict = dict()
            for key, value in serializer.errors.items():
                if key == 'paymentAmount':
                    errors_dict['Ödeme Miktarı'] = value
                elif key == 'paymentType':
                    errors_dict['Ödeme Tipi'] = value

            return Response(errors_dict, status=status.HTTP_400_BAD_REQUEST)


class PaymentTypeSelectApi(APIView):
    def get(self, request, format=None):
        try:
            select_arr = []
            data = PaymentType.objects.all()

            for type in data:
                select_object = SelectObject()
                select_object.value = type.id
                select_object.label = type.name
                select_arr.append(select_object)

            serializer = SelectSerializer(select_arr, many=True, context={'request': request})

            return Response(serializer.data, status.HTTP_200_OK)
        except Exception as e:
            return Response("error", status.HTTP_500_INTERNAL_SERVER_ERROR)


class CheckingAccountApi(APIView):

    def get(self, request, format=None):
        checking_accounts = CheckingAccount.objects.filter(protocol__patient__uuid=request.GET.get('id'))
        checking_account_array = []
        for checking_account in checking_accounts:
            data = dict()
            data['checkingAccountUUID'] = checking_account.uuid
            payment_movement = PaymentMovement.objects.filter(checkingAccount_id=checking_account.id,
                                                              paymentType__name='İndirim').aggregate(
                discount=Sum('paymentAmount'))['discount']
            data['discount'] = payment_movement
            data['protocolId'] = checking_account.protocol.id
            data['remainingDebt'] = checking_account.remainingDebt
            data['date'] = checking_account.protocol.creationDate.strftime("%d-%m-%Y %H:%M:%S")
            data['total'] = checking_account.total
            data['paymentSituation'] = checking_account.paymentSituation.name
            data['protocolTaxRate'] = checking_account.protocol.taxRate
            checking_account_array.append(data)

        api_object = APIObject()
        api_object.data = checking_account_array
        api_object.recordsFiltered = checking_accounts.count()
        api_object.recordsTotal = checking_accounts.count()

        serializer = CheckingAccountPageSerializer(api_object, context={'request': request})
        return Response(serializer.data, status.HTTP_200_OK)


class PaymentMovementApi(APIView):
    def get(self, request, format=None):
        payment_movements = PaymentMovement.objects.filter(checkingAccount__uuid=request.GET.get('id')).order_by('-id')
        payment_movements_array = []
        for movement in payment_movements:
            data = dict()
            data['movementUUID'] = movement.uuid
            data['paymentAmount'] = movement.paymentAmount
            data['date'] = movement.creationDate.strftime("%d-%m-%Y %H:%M:%S")
            data['paymentTypeDesc'] = PaymentType.objects.get(id=movement.paymentType.id).name
            payment_movements_array.append(data)

        api_object = APIObject()
        api_object.data = payment_movements_array
        api_object.recordsFiltered = payment_movements.count()
        api_object.recordsTotal = payment_movements.count()

        serializer = PaymentMovementPageSerializer(api_object, context={'request': request})
        return Response(serializer.data, status.HTTP_200_OK)
