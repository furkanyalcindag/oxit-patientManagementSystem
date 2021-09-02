from django.urls import path

from pmsMobile.views.AnswerView import AnswerApi
from pmsMobile.views.CheckingAccountView import PatientCheckingAccountApi, PatientTotalCheckingAccountApi, \
    PatientPaymentMovementApi
from pmsMobile.views.AppointmentView import PatientAppointmentApi
from pmsMobile.views.BlogView import PublishBlogApi, SponsoredBlogApi
from pmsMobile.views.ClinicView import ClinicGeneralInfoApi, ClinicMediaApi
from pmsMobile.views.DoctorView import DoctorProfileApi, ClinicsDoctorsApi
from pmsMobile.views.PatientView import PatientProfileApi
from pmsMobile.views.ProtocolView import PatientProtocolApi
from pmsMobile.views.QuestionView import PatientQuestionApi, AllQuestionApi

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
    path('patient-appointment-api/', PatientAppointmentApi.as_view(), name='patient-appointment-api'),
    path('patient-checking-account-api/', PatientCheckingAccountApi.as_view(), name='patient-checking-account-api'),
    path('patient-total-checking-account-api/', PatientTotalCheckingAccountApi.as_view(),
         name='patient-total-checking-account-api'),
    path('patient-payment-movement-api/', PatientPaymentMovementApi.as_view(), name='patient-payment-movement-api'),
    path('patient-question-api/', PatientQuestionApi.as_view(), name='patient-question-api'),
    path('all-question-api/', AllQuestionApi.as_view(), name='all-question-api'),
    path('answer-api/', AnswerApi.as_view(), name='answer-api'),

]
