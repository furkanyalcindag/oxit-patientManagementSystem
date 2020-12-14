from django.conf.urls import url

from carService.Views.CarApiViews import CarApi
from carService.Views.CategoryApiViews import CategoryApi, CategorySelectApi
from carService.Views.CustomerApiViews import CustomerApi
from carService.Views.ProductApiViews import ProductApi
from carService.Views.ServiceApiVİews import ServiceTypeSelectApi, ServiceApi
from carService.Views.StaffViews import StaffApi, ServicemanSelectApi
from carService.Views.UserApiView import UserApi, GroupApi

app_name = 'carService'

urlpatterns = [

    url(r'user-api/$', UserApi.as_view(), name='user-api'),
    url(r'group-api/$', GroupApi.as_view(), name='group-api'),
    url(r'customer-api/', CustomerApi.as_view(), name='customer-api'),
    url(r'product-api/$', ProductApi.as_view(), name='product-api'),
    url(r'car-api/$', CarApi.as_view(), name='car-api'),
    url(r'category-api/$', CategoryApi.as_view(), name='category-api'),
    url(r'category-select-api/$', CategorySelectApi.as_view(), name='category-select-api'),
    url(r'service-type-select-api/$', ServiceTypeSelectApi.as_view(), name='service-type-select-api'),
    url(r'staff-api/$', StaffApi.as_view(), name='staff-api'),
    url(r'service-api/$', ServiceApi.as_view(), name='service-api'),
    url(r'serviceman-select-api/$', ServicemanSelectApi.as_view(), name='serviceman-select-api'),

    # url(r'swagger/$', views.schema_view, name='swagger'),

    # url(r'swagger/$', views.schema_view, name='swagger'),

]
