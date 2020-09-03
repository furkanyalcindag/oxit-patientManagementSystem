from django.conf.urls import url

from carService.Views.UserApiView import UserApi

app_name = 'carService'

urlpatterns = [

    url(r'user-api/$', UserApi.as_view(), name='user-api'),


]