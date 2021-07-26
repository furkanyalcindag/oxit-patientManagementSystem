from django.urls import path

from management.views.ClinicView import ClinicApi
from management.views.GroupView import GroupApi
from management.views.UserView import UserApi
from management.views.GeneralView import CityDistrictSelectApi

app_name = 'management'

urlpatterns = [

    path('clinic-api/', ClinicApi.as_view(), name='clinic-api'),
    path('group-api/', GroupApi.as_view(), name='group-api'),
    path('user-api/', UserApi.as_view(), name='user-api'),
    path('city-api/', CityDistrictSelectApi.as_view(), name='city-api'),

]
