import traceback

from django.db import transaction
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from pms.models import CheckingAccount, PaymentType, PaymentSituation
from pms.models.PaymentMovement import PaymentMovement


class PaymentSerializer(serializers.Serializer):
    checkingAccountUUID = serializers.UUIDField(write_only=True)
    paymentAmount = serializers.DecimalField(max_digits=10, decimal_places=2)
    paymentType = serializers.IntegerField(write_only=True)
    paymentTypeDesc = serializers.CharField(read_only=True)
    paymentDate = serializers.DateTimeField(read_only=True)

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        payment_movement = PaymentMovement()

        try:
            checking_account = CheckingAccount.objects.get(uuid=validated_data.get('checkingAccountUUID'))
            if checking_account.paymentSituation.name != 'Ödendi' and validated_data.get(
                    'paymentAmount') <= checking_account.remainingDebt:
                payment_type = PaymentType.objects.get(id=validated_data.get('paymentType'))
                payment_movement.checkingAccount = checking_account
                payment_movement.paymentAmount = validated_data.get('paymentAmount')
                payment_movement.paymentType = payment_type
                payment_movement.save()

                checking_account.remainingDebt = checking_account.remainingDebt - validated_data.get('paymentAmount')
                if checking_account.remainingDebt == 0:
                    checking_account.paymentSituation = PaymentSituation.objects.get(name__exact='Ödendi')
                else:
                    checking_account.paymentSituation = PaymentSituation.objects.get(name__exact='Kısmi Ödendi')
                checking_account.save()
            else:
                raise serializers.ValidationError(
                    "Ödeme miktarı toplam ücretten fazla. Lütfen ödeme miktarını kontol ediniz")

            return checking_account
        except:
            traceback.print_exc()
            raise serializers.ValidationError("Ödeme miktarı kalan toplam ücretten fazla olamaz.")


class PaymentDiscountSerializer(serializers.Serializer):
    checkingAccountUUID = serializers.UUIDField(write_only=True)
    paymentAmount = serializers.DecimalField(max_digits=10, decimal_places=2)

    def create(self, validated_data):
        payment_movement = PaymentMovement()
        try:
            checking_account = CheckingAccount.objects.get(uuid=validated_data.get('checkingAccountUUID'))
            if checking_account.paymentSituation.name == 'Ödenmedi' or checking_account.paymentSituation.name == 'Kısmi Ödendi' and validated_data.get(
                    'paymentAmount') <= checking_account.remainingDebt:
                payment_type = PaymentType.objects.get(name='İndirim')
                payment_movement.checkingAccount = checking_account
                payment_movement.paymentType = payment_type
                payment_movement.paymentAmount = validated_data.get('paymentAmount')
                payment_movement.save()
                checking_account.remainingDebt = checking_account.remainingDebt - validated_data.get('paymentAmount')
                checking_account.save()
            if checking_account.remainingDebt == 0:
                checking_account.paymentSituation = PaymentSituation.objects.get(name='Ödendi')
                checking_account.paymentSituation.save()
            return checking_account
        except:
            traceback.print_exc()
            raise serializers.ValidationError("lütfen tekrar deneyiniz")

    def update(self, instance, validated_data):
        pass


class CheckingAccountSerializer(serializers.Serializer):
    checkingAccountUUID = serializers.UUIDField(read_only=True)
    date = serializers.DateTimeField()
    remainingDebt = serializers.DecimalField(max_digits=10, decimal_places=2)
    total = serializers.DecimalField(max_digits=10, decimal_places=2)
    paymentSituation = serializers.CharField()
    discount = serializers.DecimalField(read_only=True, max_digits=10, decimal_places=2)
    protocolId = serializers.IntegerField(read_only=True)

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


class PaymentMovementSerializer(serializers.Serializer):
    movementUUID = serializers.UUIDField(read_only=True)
    date = serializers.DateTimeField()
    paymentAmount = serializers.DecimalField(max_digits=10, decimal_places=2)
    paymentTypeDesc = serializers.CharField()

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass


class PaymentMovementPageSerializer(serializers.Serializer):
    data = PaymentMovementSerializer(many=True)
    recordsTotal = serializers.IntegerField()
    recordsFiltered = serializers.IntegerField()

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass
