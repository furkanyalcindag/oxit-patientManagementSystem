from rest_framework import serializers


class AdminDashboardSerializer(serializers.Serializer):
    productCount = serializers.IntegerField()
    outOfStockCount = serializers.IntegerField()
    carCount = serializers.IntegerField()
    customerCount = serializers.IntegerField()
    #processWorkCount = serializers.IntegerField()
    uncompletedServiceCount = serializers.IntegerField()
    waitingApproveServiceCount = serializers.IntegerField()
    totalCheckingAccountDaily = serializers.DecimalField(max_digits=10, decimal_places=2)
    totalCheckingAccountMonthly = serializers.DecimalField(max_digits=10, decimal_places=2)
    totalCheckingAccountYearly = serializers.DecimalField(max_digits=10, decimal_places=2)
