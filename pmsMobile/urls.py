from django.urls import path

from pmsMobile.views.BlogView import PublishBlogApi, SponsoredBlogApi
from pmsMobile.views.ClinicView import ClinicGeneralInfoApi, ClinicMediaApi
from pmsMobile.views.DoctorView import DoctorProfileApi, ClinicsDoctorsApi
from pmsMobile.views.PatientView import PatientProfileApi
from pmsMobile.views.ProtocolView import PatientProtocolApi

app_name = 'pmsMobile'

urlpatterns = [

    path('clinic-general-info-api/', ClinicGeneralInfoApi.as_view(), name='clinic-general-info-api'),
    path('clinic-media-api/', ClinicMediaApi.as_view(), name='clinic-media-api'),
    path('doctor-profile-api/', DoctorProfileApi.as_view(), name='doctor-profile-api'),
    path('publish-blog-api/', PublishBlogApi.as_view(), name='publish-blog-api'),
    path('sponsored-blog-api/', SponsoredBlogApi.as_view(), name='sponsored-blog-api'),
    path('clinics-doctors-api/', ClinicsDoctorsApi.as_view(), name='clinics-doctors-api'),
    path('patient-profile-api/', PatientProfileApi.as_view(), name='patient-profile-api'),
    path('patient-protocol-api/', PatientProtocolApi.as_view(), name='patient-protocol-api'),
]
