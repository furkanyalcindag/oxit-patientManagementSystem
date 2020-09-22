from django.conf.urls import url

from carService import views
from carService.Views.ProductApiViews import ProductApi
from carService.Views.UserApiView import UserApi

app_name = 'carService'

urlpatterns = [

    url(r'user-api/$', UserApi.as_view(), name='user-api'),
    url(r'product-api/$', ProductApi.as_view(), name='product-api'),

    url(r'swagger/$', views.schema_view, name='swagger'),


]