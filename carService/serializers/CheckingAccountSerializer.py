import traceback

from rest_framework import serializers

from carService.models import CheckingAccount, PaymentType, PaymentMovement, PaymentSituation
from carService.serializers.GeneralSerializer import ButtonSerializer


class CheckingAccountSerializer(serializers.Serializer):
    checkingAccountId = serializers.UUIDField(read_only=True)
    serviceDate = serializers.DateTimeField()
    plate = serializers.CharField()
    customerName = serializers.CharField()
    remainingPrice = serializers.DecimalField(max_digits=10, decimal_places=2)
    totalPrice = serializers.DecimalField(max_digits=10, decimal_places=2)
    buttons = ButtonSerializer(many=True, read_only=True)

    paymentSituation = serializers.CharField()

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass


class CheckingAccountPageSerializer(serializers.Serializer):
    data = CheckingAccountSerializer(many=True)
    recordsTotal = serializers.IntegerField()
    recordsFiltered = serializers.IntegerField()

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass


class PaymentSerializer(serializers.Serializer):
    checkingAccountUUID = serializers.UUIDField(write_only=True)
    paymentAmount = serializers.DecimalField(max_digits=10, decimal_places=2)
    paymentType = serializers.IntegerField(write_only=True)
    paymentTypeDesc = serializers.CharField(read_only=True)
    paymentDate = serializers.DateTimeField(read_only=True)

    def create(self, validated_data):
        payment_movement = PaymentMovement()
        try:
            checking_account = CheckingAccount.objects.get(uuid=validated_data.get('checkingAccountUUID'))
            if checking_account.paymentSituation.name != 'Ödendi' and validated_data.get(
                    'paymentAmount') <= checking_account.remainingDebt:
                payment_type = PaymentType.objects.get(pk=validated_data.get('paymentType'))
                payment_movement.checkingAccount = checking_account
                payment_movement.paymentAmount = validated_data.get('paymentAmount')
                payment_movement.paymentType = payment_type
                payment_movement.save()

                checking_account.remainingDebt = checking_account.remainingDebt-validated_data.get('paymentAmount')

                if checking_account.remainingDebt == validated_data.get('paymentAmount'):
                    checking_account.paymentSituation = PaymentSituation.objects.get(name__exact='Ödendi')
                else:
                    checking_account.paymentSituation = PaymentSituation.objects.get(name__exact='Kısmi Ödendi')

                checking_account.save()

            return checking_account





        except:
            traceback.print_exc()
            raise serializers.ValidationError("lütfen tekrar deneyiniz")

    def update(self, instance, validated_data):
        pass
