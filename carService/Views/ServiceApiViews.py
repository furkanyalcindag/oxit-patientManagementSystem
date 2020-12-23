import traceback

from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from carService.models import Service, Car, ServiceSituation, Profile, ServiceProduct, Product, ServiceImage, Situation
from carService.models.ApiObject import APIObject
from carService.models.SelectObject import SelectObject
from carService.models.ServiceType import ServiceType
from carService.serializers.GeneralSerializer import SelectSerializer
from carService.serializers.ProductSerializer import ProductSerializer
from carService.serializers.ServiceSerializer import ServicePageSerializer, ServiceSerializer, ServiceImageSerializer


class ServiceApi(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        data = Service.objects.filter(car=Car.objects.get(uuid=request.GET.get('carId'))).order_by('-id')
        api_object = APIObject()
        api_object.data = data
        api_object.recordsFiltered = data.count()
        api_object.recordsTotal = data.count()
        serializer = ServicePageSerializer(api_object, context={'request': request})
        return Response(serializer.data, status.HTTP_200_OK)

    def post(self, request, format=None):

        serializer = ServiceSerializer(data=request.data, context={'request': request})

        if serializer.is_valid():
            serializer.save()
            return Response({"message": "service is created"}, status=status.HTTP_200_OK)
        else:

            errors_dict = dict()
            for key, value in serializer.errors.items():
                if key == 'serviceType':
                    errors_dict['Servis Tipi'] = value
                elif key == 'serviceKM':
                    errors_dict['KM'] = value
                elif key == 'complaint':
                    errors_dict['Şikayet'] = value
                elif key == 'responsiblePerson':
                    errors_dict['Sorumlu Kişi'] = value
                elif key == 'serviceman':
                    errors_dict['Usta'] = value

            return Response(errors_dict, status=status.HTTP_400_BAD_REQUEST)


class ServiceTypeSelectApi(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        service_types = ServiceType.objects.all()
        service_types_objects = []
        select_object_root = SelectObject()
        select_object_root.label = "Seçiniz"
        select_object_root.value = ""
        service_types_objects.append(select_object_root)

        for service_type in service_types:
            select_object = SelectObject()
            select_object.label = service_type.name
            select_object.value = service_type.id
            service_types_objects.append(select_object)

        serializer = SelectSerializer(service_types_objects, many=True, context={'request': request})
        return Response(serializer.data, status.HTTP_200_OK)


class GetCarServicesApi(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        car = Car.objects.get(uuid=request.GET.get('uuid'))
        services = Service.objects.filter(car=car).order_by('-id')
        service_array = []

        for service in services:
            data = dict()
            data['serviceType'] = service.serviceType.name
            data['carUUID'] = request.GET.get('uuid')
            data['serviceKM'] = service.serviceKM
            data['complaint'] = service.complaint
            data['serviceSituation'] = ServiceSituation.objects.filter(service=service).order_by('-id')[:1][
                0].situation.name
            data['creationDate'] = service.creationDate.strftime("%d-%m-%Y %H:%M:%S")
            data['serviceman'] = service.serviceman.user.first_name + ' ' + service.serviceman.user.last_name
            service_array.append(data)

        serializer = ServiceSerializer(service_array, many=True, context={'request': request})
        return Response(serializer.data, status.HTTP_200_OK)


class GetServicesApi(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        user = User.objects.get(id=request.user.id)
        group_name = request.user.groups.filter()[0].name
        services = dict()
        if group_name == 'Tamirci':
            services = Service.objects.filter(serviceman__user=user).order_by('-id')
        elif group_name == 'Admin':
            services = Service.objects.filter().order_by('-id')
        elif group_name == 'Customer':
            cars = Car.objects.filter(profile=Profile.objects.get(user=user))
            services = Service.objects.filter(car__in=cars).order_by('-id')

        services = Service.objects.filter().order_by('-id')
        service_array = []

        for service in services:
            data = dict()
            data['uuid'] = service.uuid
            data['serviceType'] = service.serviceType.name
            data['carUUID'] = service.car.uuid
            data['serviceKM'] = service.serviceKM
            data['complaint'] = service.complaint
            data['serviceSituation'] = ServiceSituation.objects.filter(service=service).order_by('-id')[:1][
                0].situation.name
            data['creationDate'] = service.creationDate.strftime("%d-%m-%Y %H:%M:%S")
            data['plate'] = service.car.plate
            data['responsiblePerson'] = service.responsiblePerson
            data['serviceman'] = service.serviceman.user.first_name + ' ' + service.serviceman.user.last_name
            service_array.append(data)

        api_object = APIObject()
        api_object.data = service_array
        api_object.recordsFiltered = services.count()
        api_object.recordsTotal = services.count()
        serializer = ServicePageSerializer(api_object, context={'request': request})

        # serializer = ServiceSerializer(service_array, many=True, context={'request': request})
        return Response(serializer.data, status.HTTP_200_OK)


class GetServiceDetailApi(APIView):
    # permission_classes = (IsAuthenticated,)
    def get(self, request, format=None):
        services = dict()

        service = Service.objects.get(uuid=request.GET.get('uuid'))
        service_array = []
        data = dict()
        data['uuid'] = service.uuid
        data['serviceType'] = service.serviceType.name
        data['carUUID'] = service.car.uuid
        data['serviceKM'] = service.serviceKM
        data['complaint'] = service.complaint
        data['serviceSituation'] = ServiceSituation.objects.filter(service=service).order_by('-id')[:1][
            0].situation.name
        data['creationDate'] = service.creationDate.strftime("%d-%m-%Y %H:%M:%S")
        data['plate'] = service.car.plate
        data['responsiblePerson'] = service.responsiblePerson
        data['serviceman'] = service.serviceman.user.first_name + ' ' + service.serviceman.user.last_name
        data['price'] = service.price
        data['totalPrice'] = service.totalPrice
        serializer = ServiceSerializer(data, context={'request': request})

        # serializer = ServiceSerializer(service_array, many=True, context={'request': request})
        return Response(serializer.data, status.HTTP_200_OK)


class DeterminationServiceApi(APIView):
    # permission_classes = (IsAuthenticated,)
    def post(self, request, format=None):
        try:
            products = request.data['products']
            photos = request.data['photos']
            uuid = request.data['uuid']
            determination = request.data['determination'] if request.data['determination'] is not None else ''
            service = Service.objects.get(uuid=uuid)
            service.description = determination
            service.save()

            net_price = 0
            total_price = 0
            for product in products:
                productObj = Product.objects.get(uuid=product['uuid'])
                serviceProduct = ServiceProduct()
                serviceProduct.product = productObj
                serviceProduct.service = service
                serviceProduct.productNetPrice = productObj.netPrice
                serviceProduct.productTaxRate = productObj.taxRate
                serviceProduct.quantity = 1
                serviceProduct.productTotalPrice = productObj.netPrice + (
                        productObj.netPrice * productObj.taxRate / 100)
                net_price = net_price + serviceProduct.productNetPrice
                total_price = total_price + serviceProduct.productTotalPrice
                serviceProduct.save()

            for photo in photos:
                serviceImage = ServiceImage()
                serviceImage.service = service
                serviceImage.image = photo['path']
                serviceImage.save()

            situation = Situation.objects.get(name__exact='Müşteri Onayı Bekleniyor')
            service_situation = ServiceSituation()
            service_situation.service = service
            service_situation.situation = situation
            service_situation.save()
            service.price = net_price
            service.totalPrice = total_price
            service.save()

            return Response("Başarılı", status.HTTP_200_OK)

        except:
            traceback.print_exc()
            return Response("Başarısız", status.HTTP_400_BAD_REQUEST)


class GetServiceProductsApi(APIView):
    # permission_classes = (IsAuthenticated,)
    def get(self, request, format=None):
        service = Service.objects.get(uuid=request.GET.get('uuid'))
        service_products = ServiceProduct.objects.filter(service=service)
        products = []
        for serviceProduct in service_products:
            product = serviceProduct.product
            product.netPrice = serviceProduct.productNetPrice
            product.totalProduct = serviceProduct.productTotalPrice
            product.taxRate = serviceProduct.productTaxRate
            product.quantity = serviceProduct.quantity
            products.append(product)

        serializer = ProductSerializer(products, many=True, context={'request': request})
        return Response(serializer.data, status.HTTP_200_OK)


class GetServiceImagesApi(APIView):
    # permission_classes = (IsAuthenticated,)
    def get(self, request, format=None):
        service = Service.objects.get(uuid=request.GET.get('uuid'))
        service_images = ServiceImage.objects.filter(service=service)
        images = []
        for image in service_images:
            data = dict()
            data['image'] = image.image
            images.append(data)

        serializer = ServiceImageSerializer(images, many=True, context={'request': request})
        return Response(serializer.data, status.HTTP_200_OK)
