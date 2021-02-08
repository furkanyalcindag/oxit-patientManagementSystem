import datetime

from django.db.models import Q

from carService.models import Product, Car, Profile, Service, ServiceSituation, Situation, PaymentMovement


def get_product_count():
    return Product.objects.filter(isDeleted=False).count()


def get_product_out_of_stock_count():
    return Product.objects.filter(isDeleted=False).filter(quantity__exact=0).count()


def get_car_count():
    return Car.objects.filter(isDeleted=False).count()


def get_customer_count():
    return Profile.objects.filter(user__groups__name__exact='Customer').count()


def get_process_work_count():
    return Service.objects.filter()


def get_uncompleted_services_count():
    # x = ServiceSituation.objects.all().order_by('service', '-id').distinct('service').values()
    x = ServiceSituation.objects.order_by('service', '-id').distinct('service')
    return ServiceSituation.objects.filter(id__in=x).filter(situation=Situation.objects.get(name__exact='İşlemde'))


def get_waiting_approve_services_count():
    # x = ServiceSituation.objects.all().order_by('service', '-id').distinct('service').values()
    x = ServiceSituation.objects.order_by('service', '-id').distinct('service')
    return ServiceSituation.objects.filter(id__in=x).filter(
        situation=Situation.objects.get(name__exact='Müşteri Onayı Bekleniyor')).count()


def get_completed_services_count():
    # x = ServiceSituation.objects.all().order_by('service', '-id').distinct('service').values()
    x = ServiceSituation.objects.order_by('service', '-id').distinct('service')
    return ServiceSituation.objects.filter(id__in=x).filter(
        situation=Situation.objects.get(Q(name__exact='Tamamlandı')) | Q(name__exact='TeslimEdildi')).count()


def get_total_checking_account(type):
    today = datetime.date.today()
    today_min = datetime.datetime.combine(datetime.date.today(), datetime.time.min)
    today_max = datetime.datetime.combine(datetime.date.today(), datetime.time.max)

    if type=='monthly':

        print(1)
    elif type=='daily':
        PaymentMovement.objects.filter(creationDate__range=(today_min,tod))
        print(2)
    elif type=='yearly':

