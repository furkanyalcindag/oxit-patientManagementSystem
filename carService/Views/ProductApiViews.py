from rest_framework import status
from rest_framework.permissions import IsAuthenticated, BasePermissionMetaclass
from rest_framework.views import APIView

from carService.models import Product
from carService.serializers.ProductSerializer import ProductSerializer
from rest_framework.response import Response


class ProductApi(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        data = Product.objects.all()
        serializer = ProductSerializer(data, many=True, context={'request': request})
        return Response(serializer.data, status.HTTP_200_OK)
