from rest_framework import status
from rest_framework.permissions import IsAuthenticated, BasePermissionMetaclass
from rest_framework.views import APIView

from carService.models import Product
from carService.serializers.ProductSerializer import ProductSerializer, ProductSerializerr
from rest_framework.response import Response


class ProductApi(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        data = Product.objects.all().order_by('-id')
        serializer = ProductSerializer(data, many=True, context={'request': request})
        return Response(serializer.data, status.HTTP_200_OK)

    def post(self, request, format=None):
        serializer = ProductSerializerr(data=request.data, context={'request': request})

        if serializer.is_valid():
            serializer.save()
            return Response({"message": "product is created"}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

