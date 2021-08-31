# oxit doctor view
import calendar
import datetime
import traceback

from django.db.models import Sum, Q
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

from pms.models import PaymentType, CheckingAccount, PaymentMovement
from pmsMobile.models.APIObject import APIObject
from pmsMobile.serializers.CheckingAccountSerializer import CheckingAccountPageSerializer, \
    PaymentMovementPageSerializer


class PatientCheckingAccountApi(APIView):

    def get(self, request, format=None):
        checking_accounts = CheckingAccount.objects.filter(protocol__patient__profile__user=request.user)
        remainingDebt_sum = \
            CheckingAccount.objects.filter(protocol__patient__profile__user=request.user).aggregate(
                Sum('remainingDebt'))[
                'remainingDebt__sum']
        total_sum = \
            CheckingAccount.objects.filter(protocol__patient__profile__user=request.user).aggregate(Sum('total'))[
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


class PatientPaymentMovementApi(APIView):
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


class PatientTotalCheckingAccountApi(APIView):

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
            last = datetime.datetime(int(given_date.year), int(given_date.month), int(last_day_of_month), 23, 59, 59)

            first_yearly = datetime.datetime(int(given_date.year), int(1), int(1))
            last_yearly = datetime.datetime(int(given_date.year), int(12), int(last_day_of_month), 23, 59, 59)
            monthly_total_price = CheckingAccount.objects.filter(protocol__patient__profile__user=request.user).filter(
                ~Q(paymentSituation__name='Ödendi')).filter(creationDate__range=(first, last)).aggregate(Sum('total'))[
                'total__sum']
            daily_total_price = CheckingAccount.objects.filter(protocol__patient__profile__user=request.user).filter(
                ~Q(paymentSituation__name='Ödendi')).filter(creationDate__range=(today_min, today_max)).aggregate(
                Sum('total'))['total__sum']
            yearly_total_price = CheckingAccount.objects.filter(protocol__patient__profile__user=request.user).filter(
                ~Q(paymentSituation__name='Ödendi')).filter(creationDate__range=(first_yearly, last_yearly)).aggregate(
                Sum('total'))['total__sum']
            monthly_remaining_debt = \
                CheckingAccount.objects.filter(protocol__patient__profile__user=request.user).filter(
                    ~Q(paymentSituation__name='Ödendi')).filter(
                    creationDate__range=(first, last)).aggregate(
                    Sum('remainingDebt'))['remainingDebt__sum']
            daily_remaining_debt = CheckingAccount.objects.filter(protocol__patient__profile__user=request.user).filter(
                ~Q(paymentSituation__name='Ödendi')).filter(
                creationDate__range=(today_min, today_max)).aggregate(
                Sum('remainingDebt'))['remainingDebt__sum']
            yearly_remaining_debt = \
                CheckingAccount.objects.filter(protocol__patient__profile__user=request.user).filter(
                    ~Q(paymentSituation__name='Ödendi')).filter(
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
