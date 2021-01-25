import traceback
from decimal import Decimal

from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from carService.models import Service, Car, ServiceSituation, Profile, ServiceProduct, Product, ServiceImage, Situation, \
    CheckingAccount, PaymentSituation
from carService.models.ApiObject import APIObject
from carService.models.SelectObject import SelectObject
from carService.models.ServiceType import ServiceType
from carService.serializers.GeneralSerializer import SelectSerializer
from carService.serializers.ProductSerializer import ProductSerializer
from carService.serializers.ServiceSerializer import ServicePageSerializer, ServiceSerializer, ServiceImageSerializer
from carService.services import ButtonServices


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
            data['id'] = service.pk
            data['serviceType'] = service.serviceType.name
            data['carUUID'] = request.GET.get('uuid')
            data['serviceKM'] = service.serviceKM
            data['complaint'] = service.complaint
            data['serviceSituation'] = ServiceSituation.objects.filter(service=service).order_by('-id')[:1][
                0].situation.name
            data['creationDate'] = service.creationDate.strftime("%d-%m-%Y %H:%M:%S")
            data['serviceman'] = service.serviceman.user.first_name + ' ' + service.serviceman.user.last_name
            data['camera'] = None
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
            profile = Profile.objects.get(user=user)
            services = Service.objects.filter(serviceman=profile).order_by('-id')
        elif group_name == 'Admin':
            services = Service.objects.filter().order_by('-id')
        elif group_name == 'Customer':
            cars = Car.objects.filter(profile=Profile.objects.get(user=user))
            services = Service.objects.filter(car__in=cars).order_by('-id')

        # services = Service.objects.filter().order_by('-id')
        service_array = []

        for service in services:
            data = dict()
            data['id'] = "#" + str(service.pk)
            situation_name = ServiceSituation.objects.filter(service=service).order_by('-id')[:1][
                0].situation.name
            data['uuid'] = service.uuid
            data['serviceType'] = service.serviceType.name
            data['carUUID'] = service.car.uuid
            data['serviceKM'] = service.serviceKM
            data['complaint'] = service.complaint
            data['serviceSituation'] = situation_name
            data['creationDate'] = service.creationDate.strftime("%d-%m-%Y %H:%M:%S")
            data['plate'] = service.car.plate
            data['responsiblePerson'] = service.responsiblePerson
            data['serviceman'] = service.serviceman.user.first_name + ' ' + service.serviceman.user.last_name
            data['camera']=None

            data['buttons'] = ButtonServices.get_buttons(group_name, situation_name, service)

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
        data['laborPrice'] = service.laborPrice
        data['laborTaxRate'] = service.laborTaxRate
        data['laborName'] = service.laborName
        data['camera'] =None
        if service.receiverPerson is None:
            data['receiverPerson'] = '-'
        else:
            data['receiverPerson'] = service.receiverPerson
        if service.description is None:
            data['description'] = '-'
        else:
            data['description'] = service.description
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
            labor_price = Decimal(request.data['laborPrice'])
            labor_tax_rate = Decimal(request.data['laborTaxRate'])
            labor_name = request.data['laborName']
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
            service.price = net_price + labor_price
            service.totalPrice = total_price
            service.laborPrice = labor_price
            service.laborTaxRate = labor_tax_rate
            service.laborName = labor_name
            service.totalPrice = service.totalPrice + labor_price + (labor_price * labor_tax_rate / 100)
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


class ServiceCustomerAcceptApi(APIView):

    # permission_classes = (IsAuthenticated,)
    def post(self, request, format=None):

        try:
            service = Service.objects.get(uuid=request.data['uuid'])
            is_accept = request.data['isAccept']

            if is_accept:
                service_situation = ServiceSituation()
                service_situation.service = service
                service_situation.situation = Situation.objects.get(name='İşlem Bekleniyor')
                service_situation.save()
                return Response("Servis Onaylandı", status.HTTP_200_OK)
            else:
                service_situation = ServiceSituation()
                service_situation.service = service
                service_situation.situation = Situation.objects.get(name='İptal Edildi')
                service_situation.save()
                return Response("Servis İptal Edildi", status.HTTP_200_OK)
        except:
            traceback.print_exc()
            return Response("Servis ", status.HTTP_400_BAD_REQUEST)


class ServiceProcessingApi(APIView):
    # permission_classes = (IsAuthenticated,)
    def post(self, request, format=None):
        try:
            service = Service.objects.get(uuid=request.data['uuid'])
            situation_no = request.data['situationNo']
            service_situation = ServiceSituation()
            service_situation.service = service

            '''
                     situation_no
                     1=>İşleme Al
                     2=>İşlem Tamamla
                     3=>Teslim Et
                     '''
            if situation_no == 1:
                situation = Situation.objects.get(name__exact='İşlemde')
                service_situation.situation = situation
                service_situation.save()
            elif situation_no == 2:
                situation = Situation.objects.get(name__exact='Tamamlandı')
                service_situation.situation = situation
                service_situation.save()
                checking_account = CheckingAccount()
                checking_account.service = service
                checking_account.remainingDebt = service.totalPrice
                checking_account.paymentSituation = PaymentSituation.objects.get(name__exact='Ödenmedi')
                checking_account.save()

            elif situation_no == 3:
                situation = Situation.objects.get(name__exact='Teslim Edildi')
                service_situation.situation = situation
                service_situation.save()
                receiver_person = request.data['receiverPerson']
                service.receiverPerson = receiver_person
                service.save()

            return Response("Servis ", status.HTTP_200_OK)

        except:
            traceback.print_exc()
            return Response("Servis ", status.HTTP_400_BAD_REQUEST)
