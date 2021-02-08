import json

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from carService.serializers.DashboardSerializer import AdminDashboardSerializer
from carService.services import DashboardServices


class AdminDashboardViews(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        data = dict()
        data['productCount'] = DashboardServices.get_product_count()
        data['outOfStockCount'] = DashboardServices.get_product_out_of_stock_count()
        data['carCount'] = DashboardServices.get_car_count()
        data['customerCount'] = DashboardServices.get_customer_count()
        #data['processWorkCount'] = DashboardServices.get_process_work_count()
        data['uncompletedServiceCount'] = DashboardServices.get_uncompleted_services_count()
        data['waitingApproveServiceCount'] = DashboardServices.get_waiting_approve_services_count()
        data['completedServiceCount'] = DashboardServices.get_completed_services_count()
        data['totalCheckingAccountDaily'] = DashboardServices.get_total_checking_account('daily')
        data['totalCheckingAccountMonthly'] = DashboardServices.get_total_checking_account('monthly')
        data['totalCheckingAccountYearly'] = DashboardServices.get_total_checking_account('yearly')
        serializer = AdminDashboardSerializer(data, context={'request': request})
        return Response(serializer.data, status.HTTP_200_OK)
