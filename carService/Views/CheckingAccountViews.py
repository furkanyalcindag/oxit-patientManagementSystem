from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from carService.models import CheckingAccount
from carService.models.ApiObject import APIObject
from carService.serializers.CheckingAccountSerializer import CheckingAccountPageSerializer


class CheckingAccountApi(APIView):
    # permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        checking_accounts = CheckingAccount.objects.all().order_by('-id')
        checking_account_array = []
        for checking_account in checking_accounts:
            data = dict()
            data['plate'] = checking_account.service.car.plate
            data['serviceDate'] = checking_account.service.creationDate
            data['customerName'] = checking_account.service.car.profile.firmName \
                if checking_account.service.car.profile.isCorporate \
                else checking_account.service.car.profile.user.first_name + ' ' + checking_account.service.car.profile \
                .user.last_name
            data['totalPrice'] = checking_account.service.totalPrice
            data['remainingPrice'] = checking_account.remainingDebt
            data['paymentSituation'] = checking_account.paymentSituation.name

        api_object = APIObject()
        api_object.data = checking_account_array
        api_object.recordsFiltered = checking_accounts.count()
        api_object.recordsTotal = checking_accounts.count()

        serializer = CheckingAccountPageSerializer(api_object, context={'request': request})
        return Response(serializer.data, status.HTTP_200_OK)
