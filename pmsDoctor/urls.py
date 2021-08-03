from django.urls import path

from pmsDoctor.views.DepartmentView import DepartmentSelectApi
from pmsDoctor.views.DoctorView import DoctorApi, DoctorSelectApi
from pmsDoctor.views.SecretaryView import SecretaryApi
from pmsDoctor.views.GenderView import GenderSelectApi
from pmsDoctor.views.PatientView import PatientApi, PatientSelectApi
from pmsDoctor.views.BloodGroupView import BloodGroupSelectApi
from pmsDoctor.views.AppointmentView import AppointmentApi, AppointmentCalendarApi

app_name = 'pmsDoctor'

urlpatterns = [

    path('department-api/', DepartmentSelectApi.as_view(), name='department-api'),
    path('doctor-api/', DoctorApi.as_view(), name='doctor-api'),
    path('secretary-api/', SecretaryApi.as_view(), name='secretary-api'),
    path('gender-api/', GenderSelectApi.as_view(), name='gender-api'),
    path('patient-api/', PatientApi.as_view(), name='patient-api'),
    path('blood-api/', BloodGroupSelectApi.as_view(), name='blood-api'),
    path('doctor-select-api/', DoctorSelectApi.as_view(), name='doctor-select-api'),
    path('patient-select-api/', PatientSelectApi.as_view(), name='patient-select-api'),
    path('appointment-api/', AppointmentApi.as_view(), name='appointment-api'),
    path('appointment-calendar-api/', AppointmentCalendarApi.as_view(), name='appointment-calendar-api'),

]
