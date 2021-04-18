from django.conf.urls import url
from django.urls import path
from django.views.generic import TemplateView
from rest_framework_swagger.views import get_swagger_view

from career.Views.StudentViews import StudentApi

app_name = 'career'

urlpatterns = [

    url(r'student-api/$', StudentApi.as_view()),



]
