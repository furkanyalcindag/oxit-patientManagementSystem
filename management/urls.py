from django.urls import path

from management.views.ClinicView import ClinicApi
from management.views.GroupView import GroupApi
from management.views.NotificationView import NotificationApi
from management.views.UserView import UserApi
from management.views.GeneralView import CityDistrictSelectApi
from management.views.StaffView import StaffApi
from management.views.CompanyView import CompanyApi, CompanySelectApi
from management.views.AdvertisingView import AdvertisingApi, AdvertisingSelectApi
from management.views.CompanyAdvertising import CompanyAdvertisingApi

app_name = 'management'

urlpatterns = [

    path('clinic-api/', ClinicApi.as_view(), name='clinic-api'),
    path('group-api/', GroupApi.as_view(), name='group-api'),
    path('user-api/', UserApi.as_view(), name='user-api'),
    path('city-api/', CityDistrictSelectApi.as_view(), name='city-api'),
    path('staff-api/', StaffApi.as_view(), name='staff-api'),
    path('notification-api/', NotificationApi.as_view(), name='notification-api'),
    path('company-api/', CompanyApi.as_view(), name='company-api'),
    path('advertising-api/', AdvertisingApi.as_view(), name='advertising-api'),
    path('advertising-select-api/', AdvertisingSelectApi.as_view(), name='advertising-select-api'),
    path('company-select-api/', CompanySelectApi.as_view(), name='company-select-api'),
    path('company-advertising-api/', CompanyAdvertisingApi.as_view(), name='company-advertising-api'),

]
