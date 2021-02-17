
# -*- coding: utf-8 -*-
import traceback
from decimal import Decimal

from django.contrib.auth.models import User
from django.db import transaction
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView


from carService.exceptions import OutOfStockException

from django.http import FileResponse

from carService.models import Service, Car, ServiceSituation, Profile, ServiceProduct, Product, ServiceImage, Situation, \
    CheckingAccount, PaymentSituation
from carService.models.ApiObject import APIObject
from carService.models.SelectObject import SelectObject
from carService.models.ServiceType import ServiceType
from carService.serializers.GeneralSerializer import SelectSerializer
from carService.serializers.ProductSerializer import ProductSerializer
from carService.serializers.ServiceSerializer import ServicePageSerializer, ServiceSerializer, ServiceImageSerializer
from carService.services import ButtonServices
from weasyprint import HTML, CSS
import datetime
from carService.permissions import IsAccountant,IsAccountantOrAdmin,IsAdmin,IsCustomer,IsCustomerOrAdmin,IsServiceman,IsServicemanOrAdmin,method_permission_classes
class ServiceApi(APIView):
    permission_classes = (IsAuthenticated,)
    
    @method_permission_classes((IsServicemanOrAdmin|IsCustomer,))
    def get(self, request, format=None):
        data = Service.objects.filter(car=Car.objects.get(
            uuid=request.GET.get('carId'))).order_by('-id')
        api_object = APIObject()
        api_object.data = data
        api_object.recordsFiltered = data.count()
        api_object.recordsTotal = data.count()
        serializer = ServicePageSerializer(
            api_object, context={'request': request})
        return Response(serializer.data, status.HTTP_200_OK)
    
    @method_permission_classes((IsAdmin,))
    def post(self, request, format=None):

        serializer = ServiceSerializer(
            data=request.data, context={'request': request})

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
    permission_classes = (IsAuthenticated,IsAdmin,)

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

        serializer = SelectSerializer(
            service_types_objects, many=True, context={'request': request})
        return Response(serializer.data, status.HTTP_200_OK)

class GetCarServicesApi(APIView):
    permission_classes = (IsAuthenticated,IsCustomerOrAdmin|IsServiceman,)

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
            data['creationDate'] = service.creationDate.strftime(
                "%d-%m-%Y %H:%M:%S")
            data['serviceman'] = service.serviceman.user.first_name + \
                ' ' + service.serviceman.user.last_name
            data['camera'] = None
            service_array.append(data)

        serializer = ServiceSerializer(
            service_array, many=True, context={'request': request})
        return Response(serializer.data, status.HTTP_200_OK)


class GetServicesApi(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        user = User.objects.get(id=request.user.id)
        group_name = request.user.groups.filter()[0].name
        services = dict()
        if group_name == 'Tamirci':
            profile = Profile.objects.get(user=user)
            services = Service.objects.filter(
                serviceman=profile).order_by('-id')
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
            data['creationDate'] = service.creationDate.strftime(
                "%d-%m-%Y %H:%M:%S")
            data['plate'] = service.car.plate
            data['responsiblePerson'] = service.responsiblePerson

            data['serviceman'] = service.serviceman.user.first_name + ' ' + service.serviceman.user.last_name


            data['camera'] = None

            data['buttons'] = ButtonServices.get_buttons(
                group_name, situation_name, service)

            service_array.append(data)

        api_object = APIObject()
        api_object.data = service_array
        api_object.recordsFiltered = services.count()
        api_object.recordsTotal = services.count()
        serializer = ServicePageSerializer(
            api_object, context={'request': request})

        # serializer = ServiceSerializer(service_array, many=True, context={'request': request})
        return Response(serializer.data, status.HTTP_200_OK)

class GetServiceDetailApi(APIView):
    permission_classes = (IsAuthenticated,IsServicemanOrAdmin|IsCustomer,)

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
        data['creationDate'] = service.creationDate.strftime(
            "%d-%m-%Y %H:%M:%S")
        data['plate'] = service.car.plate
        data['responsiblePerson'] = service.responsiblePerson
        data['serviceman'] = service.serviceman.user.first_name + \
            ' ' + service.serviceman.user.last_name
        data['price'] = service.price
        data['totalPrice'] = service.totalPrice
        data['laborPrice'] = service.laborPrice
        data['laborTaxRate'] = service.laborTaxRate
        data['laborName'] = service.laborName
        data['camera'] = None
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
    permission_classes = (IsAuthenticated,IsServicemanOrAdmin,)

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

            situation = Situation.objects.get(
                name__exact='Müşteri Onayı Bekleniyor')
            service_situation = ServiceSituation()
            service_situation.service = service
            service_situation.situation = situation
            service_situation.save()
            service.price = net_price + labor_price
            service.totalPrice = total_price
            service.laborPrice = labor_price
            service.laborTaxRate = labor_tax_rate
            service.laborName = labor_name
            service.totalPrice = service.totalPrice + \
                labor_price + (labor_price * labor_tax_rate / 100)
            service.save()

            return Response("Başarılı", status.HTTP_200_OK)

        except:
            traceback.print_exc()
            return Response("Başarısız", status.HTTP_400_BAD_REQUEST)

class GetServiceProductsApi(APIView):
    permission_classes = (IsAuthenticated,IsServicemanOrAdmin|IsCustomer,)

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

        serializer = ProductSerializer(
            products, many=True, context={'request': request})
        return Response(serializer.data, status.HTTP_200_OK)


class GetServiceImagesApi(APIView):
    permission_classes = (IsAuthenticated,IsServicemanOrAdmin|IsCustomer,)

    def get(self, request, format=None):
        service = Service.objects.get(uuid=request.GET.get('uuid'))
        service_images = ServiceImage.objects.filter(service=service)
        images = []
        for image in service_images:
            data = dict()
            data['image'] = image.image
            images.append(data)

        serializer = ServiceImageSerializer(
            images, many=True, context={'request': request})
        return Response(serializer.data, status.HTTP_200_OK)



class GetServicePdfApi(APIView):
    permission_classes = (IsAuthenticated,IsAdmin,)
    def get(self, request, format=None):
        service = Service.objects.get(uuid=request.GET.get('uuid'))
        situation = ServiceSituation.objects.filter(service=service).order_by('-id')[:1][
                0].situation.name
        if situation == "Teslim Edildi":
            car = Car.objects.get(uuid=service.car.uuid)
            service_products = ServiceProduct.objects.filter(service=service)
            products = []
            service_images = ServiceImage.objects.filter(service=service)
            images = ""
            for image in service_images:
                html_tagged = '''<img class="car-image" src='''+image.image+'''></img>''' 
                images += html_tagged
            for serviceProduct in service_products:
                product = serviceProduct.product
                product.netPrice = serviceProduct.productNetPrice
                product.totalProduct = serviceProduct.productTotalPrice
                product.taxRate = serviceProduct.productTaxRate
                product.quantity = serviceProduct.quantity
                products.append(product)
            labor = ServiceProduct.product
            labor.barcodeNumber = '-'
            labor.name= service.laborName
            labor.brand= None
            labor.quantity= 1
            labor.netPrice= service.laborPrice
            labor.taxRate= service.laborTaxRate
            labor.totalProduct= (float(service.laborPrice) + (float(service.laborPrice) * float(service.laborTaxRate) / 100))
            if labor.name != None:
                products.append(labor)
            profile = car.profile
            receiver = "-"
            if service.receiverPerson != None:
                receiver = service.receiverPerson
            name = ""
            product_table = " "
            for product in products:
                brand_name = ""
                if product.brand != None:
                    brand_name = product.brand.name
                product_table = product_table + '''<tr>
                        <td>'''+product.barcodeNumber+'''</td> 
                        <td>'''+product.name+'''</td>
                        <td>'''+brand_name+'''</td> 
                        <td>'''+str(product.quantity)+'''</td>
                        <td>'''+str(product.netPrice)+'''</td>
                        <td>'''+str(product.taxRate)+'''</td>
                        <td>'''+str(product.totalProduct)+'''</td>           
                    </tr>'''
            if(profile.firmName):
                name = profile.firmName + "-" + \
                    profile.user.first_name + " " + profile.user.last_name
            else:
                name = profile.user.first_name + " " + profile.user.last_name
            serviceman = service.serviceman.user.first_name + \
                " " + service.serviceman.user.last_name
            try:
                html = HTML(string='''
                    <!DOCTYPE html>
                <html class="no-js" lang="tr">
                <head>
                    <meta charset="utf-8" />
                </head>
                <div class="header">
                    <img class="logo"  src="data:image/png;base64,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">
                </div>    
                <table>
                <caption>Servis Bilgileri</caption>
                <tr>
                    <th>Müşteri:</th> <td>'''+name+'''</td>
                    <th>Servise Getiren:</th><td>'''+service.responsiblePerson+'''</td>
                    <th>Plaka:</th> <td>'''+car.plate+'''</td>
                    <th>Teslim Alan:</th><td>''' +receiver+'''</td>        
                </tr>
                <tr>
                    <th>Servis Tipi:</th><td>''' + service.serviceType.name +'''</td>
                    <th>Giriş zamanı:</th> <td>'''+ str(service.creationDate).split(".")[0] +'''</td>
                    <th>Usta:</th><td>''' +serviceman+'''</td>
                    <th>KM:</th><td>''' +str(service.serviceKM)+''' KM</td>        
                </tr> 
                </table>
                <div class="desc-header">Şikayet:</div>
                <div class="description">'''+service.complaint+'''</div>
                <div class="desc-header">Tespit:</div> 
                <div class="description">'''+service.description+'''</div>
                <table>
                <caption>Servis  Ürün Listesi</caption>
                <tr>
                    <th>Barkod</th> 
                    <th>Ürün Adı</th>
                    <th>Marka</th> 
                    <th>Adet</th>
                    <th>Net Fiyat</th>
                    <th>KDV</th>
                    <th>Toplam Fiyat</th>    
                </tr>'''+product_table+'''
                <tr class="footer">
                    <th>Net: </th><td>'''+str(service.price) +''' ₺</td>
                    <th>Toplam: </th><td>'''+str(service.totalPrice) +''' ₺</td>
                </tr>
                </table>
                <div class="section-header"> Araç Fotoğrafları </div>
                '''
                +images+
                '''
                </html>

                ''')
                css = CSS(string='''
                .logo{
                    height:70px;
                }
                .car-image{
                    height:225px;
                    width:300px;
                }
                .header{
                    padding-bottom:20px;
                }
                .footer{
                    align-items: right;
                    text-align: right;
                }
                table caption{
                font-weight: bold;
                font-size: 16px;
                color: #fff;
                padding-top: 3px;
                padding-bottom: 2px;
                background-color: #3c4b64;
                }
                .car-image{
                    padding-top: 5px;
                    padding-bottom: 5px;
                    padding-right: 5px;
                    padding-left: 5px; 
                }
                .section-header{
                padding-top: 5px;
                padding-bottom: 4px;
                background-color: #3c4b64;
                font-weight: bold;
                font-size: 16px;
                color: #fff;
                }
                table {
                border-spacing: 0.5;
                border-collapse: collapse;
                background: white;
                overflow: hidden;
                width: 100%;
                margin: 0 auto;
                position: relative;
                }
                table * {
                position: relative;
                }
                table td,
                table th {
                padding-left: 1px;
                }
                table thead tr {
                height: 20px;
                background: #36304a;
                }
                table tbody tr {
                height: 20px;
                }
                table tbody tr:last-child {
                border: 0;
                }
                table td{
                text-align: left;    
                }
                table th {
                text-align: left;
                }
                table td.c,
                table th.c {
                text-align: center;
                }
                table td.r,
                table th.r {
                text-align: center;
                }

                tbody tr:nth-child(2n) {
                background-color: #f5f5f5;
                }

                tbody tr {
                font-size: 10px;
                color: #020203;
                line-height: 1.2;
                font-weight: unset;
                }
                .description {
                padding-top: 10px;
                padding-bottom: 10px;
                font-size: 12px;
                }
                .desc-header {
                    padding-top: 10px;
                    font-size: 14px;
                    font-weight: bold;
                }
                ''')
                html.write_pdf(
                    'tmp/report.pdf',stylesheets=[css])
                return FileResponse(open('tmp/report.pdf', 'rb'),status= status.HTTP_200_OK, content_type='application/pdf')
            except:
                raise Exception("Error While creating service detail pdf")
        else: 
            return Response("Teslim edilmeden rapor alınamaz",status= status.HTTP_403_FORBIDDEN)


class ServiceCustomerAcceptApi(APIView):
    permission_classes = (IsAuthenticated,IsCustomerOrAdmin)

    def post(self, request, format=None):

        try:
            with transaction.atomic():
                service = Service.objects.get(uuid=request.data['uuid'])
                is_accept = request.data['isAccept']

                if is_accept:
                    service_situation = ServiceSituation()
                    service_products = ServiceProduct.objects.filter(service=service)

                    for service_product in service_products:
                        product = service_product.product
                        if product.quantity > service_product.quantity:
                            product.quantity = product.quantity - service_product.quantity
                            product.save()
                        else:
                            raise OutOfStockException("Sorry, no numbers below zero")

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

        except OutOfStockException as e:
            traceback.print_exc()
            return Response("Ürünler Stokta Bulunmamaktadır ", status.HTTP_404_NOT_FOUND)



        except Exception as e:

            if is_accept:
                service_situation = ServiceSituation()
                service_situation.service = service
                service_situation.situation = Situation.objects.get(
                    name='İşlem Bekleniyor')
                service_situation.save()
                return Response("Servis Onaylandı", status.HTTP_200_OK)
            else:
                service_situation = ServiceSituation()
                service_situation.service = service
                service_situation.situation = Situation.objects.get(
                    name='İptal Edildi')
                service_situation.save()
                return Response("Servis İptal Edildi", status.HTTP_200_OK)
        except:

            traceback.print_exc()
            return Response("Servis ", status.HTTP_400_BAD_REQUEST)

# usta admin ?????
class ServiceProcessingApi(APIView):
    permission_classes = (IsAuthenticated,)

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
                checking_account.paymentSituation = PaymentSituation.objects.get(
                    name__exact='Ödenmedi')
                checking_account.save()
            #admin
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
