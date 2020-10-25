from django.conf.urls import url

from carService.Views.CarApiViews import CarApi
from carService.Views.CategoryApiViews import CategoryApi
from carService.Views.CustomerApiViews import CustomerApi
from carService.Views.ProductApiViews import ProductApi
from carService.Views.UserApiView import UserApi

app_name = 'carService'

urlpatterns = [

    url(r'user-api/$', UserApi.as_view(), name='user-api'),
    url(r'customer-api/', CustomerApi.as_view(), name='customer-api'),
    url(r'product-api/$', ProductApi.as_view(), name='product-api'),
    url(r'car-api/$', CarApi.as_view(), name='car-api'),
    url(r'category-api/$', CategoryApi.as_view(), name='category-api'),

    # url(r'swagger/$', views.schema_view, name='swagger'),

    # url(r'swagger/$', views.schema_view, name='swagger'),

]
