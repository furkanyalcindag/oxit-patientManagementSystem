from rest_framework import serializers


class CheckingAccountSerializer(serializers.Serializer):
    serviceDate = serializers.DateTimeField()
    plate = serializers.CharField()
    firmName = serializers.CharField()
    remainingPrice = serializers.DecimalField(max_digits=10, decimal_places=2)
    totalPrice = serializers.DecimalField(max_digits=10, decimal_places=2)
    customerName = serializers.CharField()
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
