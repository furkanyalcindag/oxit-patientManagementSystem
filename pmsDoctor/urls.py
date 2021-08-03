from django.urls import path

from pmsDoctor.views.DepartmentView import DepartmentSelectApi
from pmsDoctor.views.DoctorView import DoctorApi, DoctorSelectApi
from pmsDoctor.views.SecretaryView import SecretaryApi
from pmsDoctor.views.GenderView import GenderSelectApi
from pmsDoctor.views.PatientView import PatientApi
from pmsDoctor.views.BloodGroupView import BloodGroupSelectApi

app_name = 'pmsDoctor'

urlpatterns = [

    path('department-api/', DepartmentSelectApi.as_view(), name='department-api'),
    path('doctor-api/', DoctorApi.as_view(), name='doctor-api'),
    path('secretary-api/', SecretaryApi.as_view(), name='secretary-api'),
    path('gender-api/', GenderSelectApi.as_view(), name='gender-api'),
    path('patient-api/', PatientApi.as_view(), name='patient-api'),
    path('blood-api/', BloodGroupSelectApi.as_view(), name='blood-api'),
    path('doctor-select-api/', DoctorSelectApi.as_view(), name='doctor-select-api'),

]
