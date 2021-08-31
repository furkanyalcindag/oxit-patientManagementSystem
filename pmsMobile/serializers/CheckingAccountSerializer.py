import traceback

from django.db import transaction
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from pms.models import CheckingAccount, PaymentType, PaymentSituation
from pms.models.PaymentMovement import PaymentMovement


class CheckingAccountSerializer(serializers.Serializer):
    checkingAccountUUID = serializers.UUIDField(read_only=True)
    date = serializers.DateTimeField()
    remainingDebt = serializers.DecimalField(max_digits=10, decimal_places=2)
    total = serializers.DecimalField(max_digits=10, decimal_places=2)
    paymentSituation = serializers.CharField()
    discount = serializers.DecimalField(read_only=True, max_digits=10, decimal_places=2)
    protocolId = serializers.IntegerField(read_only=True)
    protocolTaxRate = serializers.DecimalField(read_only=True, max_digits=10, decimal_places=2)

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass


class CheckingAccountPageSerializer(serializers.Serializer):
    data = CheckingAccountSerializer(many=True)
    recordsTotal = serializers.IntegerField()
    recordsFiltered = serializers.IntegerField()
    remainingDebt = serializers.DecimalField(max_digits=10, decimal_places=2, required=False)
    total = serializers.DecimalField(max_digits=10, decimal_places=2, required=False)

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
