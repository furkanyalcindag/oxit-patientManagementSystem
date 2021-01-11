from rest_framework import status
from rest_framework.permissions import IsAuthenticated, BasePermissionMetaclass
from rest_framework.views import APIView

from carService.models import Product, Brand
from carService.models.ApiObject import APIObject
from carService.models.SelectObject import SelectObject
from carService.serializers.GeneralSerializer import SelectSerializer
from carService.serializers.ProductSerializer import ProductSerializer, ProductSerializerr, BrandSerializer, \
    BrandPageSerializer
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

            errors_dict = dict()
            for key, value in serializer.errors.items():
                if key == 'barcodeNumber':
                    errors_dict['Barkod'] = value
                elif key == 'name':
                    errors_dict['Ürün Adı'] = value
                elif key == 'quantity':
                    errors_dict['Stok'] = value
                elif key == 'netPrice':
                    errors_dict['Net Fiyat'] = value
                elif key == 'taxRate':
                    errors_dict['Vergi Oranı'] = value
                elif key == 'categories':
                    errors_dict['Kategori'] = value
                elif key == 'shelf':
                    errors_dict['Raf'] = value
                elif key == 'brand':
                    errors_dict['Marka'] = value
                elif key == 'purchasePrice':
                    errors_dict['Alış Fiyatı'] = value

            return Response(errors_dict, status=status.HTTP_400_BAD_REQUEST)


class SearchProductApi(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        #data = Product.objects.filter(barcodeNumber__istartswith=request.GET.get('barcode')).order_by('-id')
        data = Product.objects.filter(name__icontains=request.GET.get('barcode')).order_by('-id')
        serializer = ProductSerializer(data, many=True, context={'request': request})
        return Response(serializer.data, status.HTTP_200_OK)


class BrandApi(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        data = Brand.objects.all().order_by('-id')
        api_object = APIObject()
        api_object.data = data
        api_object.recordsFiltered = data.count()
        api_object.recordsTotal = data.count()
        serializer = BrandPageSerializer(api_object, context={'request': request})
        return Response(serializer.data, status.HTTP_200_OK)

    def post(self, request, format=None):

        serializer = BrandSerializer(data=request.data, context={'request': request})

        if serializer.is_valid():
            serializer.save()
            return Response({"message": "brand is created"}, status=status.HTTP_200_OK)
        else:

            errors_dict = dict()
            for key, value in serializer.errors.items():
                if key == 'name':
                    errors_dict['Marka'] = value

            return Response(errors_dict, status=status.HTTP_400_BAD_REQUEST)


class BrandSelectApi(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        brands = Brand.objects.all()
        brands_objects = []
        select_object_root = SelectObject()
        select_object_root.label = "Seçiniz"
        select_object_root.value = ""
        brands_objects.append(select_object_root)

        for brand in brands:
            select_object = SelectObject()
            select_object.label = brand.name
            select_object.value = brand.id
            brands_objects.append(select_object)

        serializer = SelectSerializer(brands_objects, many=True, context={'request': request})
        return Response(serializer.data, status.HTTP_200_OK)
