from django.conf.urls import url

from career.Views.InitViews import InitDataApi
from career.Views.StudentViews import StudentApi

app_name = 'career'

urlpatterns = [

    url(r'student-api/$', StudentApi.as_view()),
    url(r'initial-data-api/$', InitDataApi.as_view()),



]
