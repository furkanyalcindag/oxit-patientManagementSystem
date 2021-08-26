# oxit doctor view
import calendar
import datetime
import traceback

from django.db.models import Sum, Q
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

from pms.models import PaymentType, CheckingAccount, PaymentMovement
from pms.models.SelectObject import SelectObject
from pmsDoctor.models.APIObject import APIObject
from pmsDoctor.serializers.CheckingAccountSerializer import PaymentSerializer, PaymentDiscountSerializer, \
    CheckingAccountSerializer, CheckingAccountPageSerializer, PaymentMovementPageSerializer, \
    AllCheckingAccountSerializer
from pmsDoctor.serializers.GeneralSerializer import SelectSerializer


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


class PatientCheckingAccountApi(APIView):

    def get(self, request, format=None):
        checking_accounts = CheckingAccount.objects.filter(protocol__patient__uuid=request.GET.get('id'))
        remainingDebt_sum = \
        CheckingAccount.objects.filter(protocol__patient__uuid=request.GET.get('id')).aggregate(Sum('remainingDebt'))[
            'remainingDebt__sum']
        total_sum = \
        CheckingAccount.objects.filter(protocol__patient__uuid=request.GET.get('id')).aggregate(Sum('total'))[
            'total__sum']
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
            data['date'] = checking_account.creationDate.strftime("%d-%m-%Y %H:%M:%S")
            data['total'] = checking_account.total
            data['paymentSituation'] = checking_account.paymentSituation.name
            data['protocolTaxRate'] = checking_account.protocol.taxRate
            checking_account_array.append(data)

        api_object = APIObject()
        api_object.data = checking_account_array
        api_object.recordsFiltered = checking_accounts.count()
        api_object.recordsTotal = checking_accounts.count()
        api_object.remainingDebt = remainingDebt_sum
        api_object.total = total_sum

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


class TotalCheckingAccountApi(APIView):

    def get(self, request, format=None):
        try:
            today = datetime.date.today()
            paid_monthly = 0
            paid_daily = 0
            paid_yearly = 0

            today_min = datetime.datetime.combine(datetime.date.today(), datetime.time.min)
            today_max = datetime.datetime.combine(datetime.date.today(), datetime.time.max)
            given_date = datetime.datetime.today().date()
            first_day_of_month = given_date - datetime.timedelta(days=int(given_date.strftime("%d")) - 1)
            last_day_of_month = calendar.monthrange(given_date.year, given_date.month)[1]
            first = datetime.datetime(int(given_date.year), int(given_date.month), int(first_day_of_month.day))
            last = datetime.datetime(int(given_date.year), int(given_date.month), int(last_day_of_month))
            first_day_of_month = given_date - datetime.timedelta(days=int(given_date.strftime("%d")) - 1)
            last_day_of_mount = calendar.monthrange(given_date.year, 12)[1]

            first_yearly = datetime.datetime(int(given_date.year), int(1), int(1))
            last_yearly = datetime.datetime(int(given_date.year), int(12), int(last_day_of_mount))
            monthly_total_price = CheckingAccount.objects.filter(~Q(paymentSituation__name='Ödendi')).filter(
                creationDate__range=(first, last)).aggregate(
                Sum('total'))['total__sum']
            daily_total_price = CheckingAccount.objects.filter(~Q(paymentSituation__name='Ödendi')).filter(
                creationDate__range=(today_min, today_max)).aggregate(
                Sum('total'))['total__sum']
            yearly_total_price = CheckingAccount.objects.filter(~Q(paymentSituation__name='Ödendi')).filter(
                creationDate__range=(first_yearly, last_yearly)).aggregate(
                Sum('total'))['total__sum']
            monthly_remaining_debt = CheckingAccount.objects.filter(~Q(paymentSituation__name='Ödendi')).filter(
                creationDate__range=(first, last)).aggregate(
                Sum('remainingDebt'))['remainingDebt__sum']
            daily_remaining_debt = CheckingAccount.objects.filter(~Q(paymentSituation__name='Ödendi')).filter(
                creationDate__range=(today_min, today_max)).aggregate(
                Sum('remainingDebt'))['remainingDebt__sum']
            yearly_remaining_debt = CheckingAccount.objects.filter(~Q(paymentSituation__name='Ödendi')).filter(
                creationDate__range=(first_yearly, last_yearly)).aggregate(
                Sum('remainingDebt'))['remainingDebt__sum']

            if monthly_total_price is not None or monthly_remaining_debt is not None:
                paid_monthly = monthly_total_price - monthly_remaining_debt
            if daily_total_price is not None or daily_remaining_debt is not None:
                paid_daily = daily_total_price - daily_remaining_debt
            if yearly_total_price is not None or yearly_remaining_debt is not None:
                paid_yearly = yearly_total_price - yearly_remaining_debt
            data = dict()
            data['totalMonthly'] = monthly_total_price
            data['totalDaily'] = daily_total_price
            data['totalYearly'] = yearly_total_price
            data['remainingDebtMonthly'] = monthly_remaining_debt
            data['remainingDebtDaily'] = daily_remaining_debt
            data['remainingDebtYearly'] = yearly_remaining_debt
            data['paidMonthly'] = paid_monthly
            data['paidDaily'] = paid_daily
            data['paidYearly'] = paid_yearly

            return Response(data, status.HTTP_200_OK)
        except:
            traceback.print_exc()
            return Response("error", status.HTTP_500_INTERNAL_SERVER_ERROR)


class MomentaryCheckingAccountApi(APIView):
    def get(self, request, format=None):
        try:
            today_min = datetime.datetime.combine(datetime.date.today(), datetime.time.min)
            today_max = datetime.datetime.combine(datetime.date.today(), datetime.time.max)
            given_date = datetime.datetime.today().date()
            daily_movement = PaymentMovement.objects.filter(creationDate__range=(today_min, today_max))
            daily_movement_array = []
            for movement in daily_movement:
                data = dict()
                data['movementUUID'] = movement.uuid
                data['paymentAmount'] = movement.paymentAmount
                data['date'] = movement.creationDate.strftime("%d-%m-%Y %H:%M:%S")
                data[
                    'patient'] = movement.checkingAccount.protocol.patient.profile.user.first_name + ' ' + movement.checkingAccount.protocol.patient.profile.user.last_name
                data['paymentTypeDesc'] = PaymentType.objects.get(id=movement.paymentType.id).name
                daily_movement_array.append(data)

            return Response(daily_movement_array, status.HTTP_200_OK)
        except:
            traceback.print_exc()
            return Response("error", status.HTTP_500_INTERNAL_SERVER_ERROR)


class AllCheckingAccountApi(APIView):
    def get(self, request, format=None):
        try:

            all_checking_accounts = CheckingAccount.objects.all()

            all_checking_accounts_array = []
            for checking_account in all_checking_accounts:
                data = dict()
                data['date'] = checking_account.creationDate.strftime("%d-%m-%Y %H:%M:%S")
                data['remainingDebt'] = checking_account.remainingDebt
                data['total'] = checking_account.total
                data['patient'] = checking_account.protocol.patient.profile.user.first_name + ' ' + checking_account.protocol.patient.profile.user.last_name
                data['paymentTypeDesc'] = PaymentType.objects.get(id=checking_account.paymentSituation.id).name
                data['protocol'] = checking_account.protocol_id
                all_checking_accounts_array.append(data)
            serializer = AllCheckingAccountSerializer(all_checking_accounts_array, many=True,
                                                      context={'request': request})
            return Response(serializer.data, status.HTTP_200_OK)
        except:
            traceback.print_exc()
            return Response("error", status.HTTP_500_INTERNAL_SERVER_ERROR)
