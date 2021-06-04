from pms.Views.ClinicViews import ClinicApi
from django.conf.urls import url
from django.urls import path

app_name = 'pms'

urlpatterns = [

    # admin
    path('clinic-api/', ClinicApi.as_view()),
    ]