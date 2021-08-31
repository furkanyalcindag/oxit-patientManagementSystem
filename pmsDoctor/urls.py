from django.urls import path

from management.views.ClinicView import ClinicGeneralInfoApi, ClinicMediaApi
from pmsDoctor.views.BlogView import BlogApi, PublishBlogApi, SponsoredBlogApi
from pmsDoctor.views.CheckingAccountViews import PaymentAccountApi, PaymentTypeSelectApi, PaymentAccountDiscountApi, \
    PatientCheckingAccountApi, PaymentMovementApi, TotalCheckingAccountApi, MomentaryCheckingAccountApi, \
    AllCheckingAccountApi, AllMomentaryCheckingAccountApi
from pmsDoctor.views.DepartmentView import DepartmentSelectApi
from pmsDoctor.views.DoctorView import DoctorApi, DoctorSelectApi, DoctorGeneralInfoApi, DoctorContactInfoApi, \
    DoctorAboutApi, EducationTypeSelectApi, DoctorEducationApi, DoctorPrizeApi, DoctorArticleApi, \
    DoctorArticleTimelineApi, DoctorMediaApi, DoctorProfileApi, ClinicsDoctorsApi
from pmsDoctor.views.SecretaryView import SecretaryApi
from pmsDoctor.views.GenderView import GenderSelectApi
from pmsDoctor.views.PatientView import PatientApi, PatientSelectApi, PatientProfileApi
from pmsDoctor.views.BloodGroupView import BloodGroupSelectApi
from pmsDoctor.views.AppointmentView import AppointmentApi, AppointmentCalendarApi
from pmsDoctor.views.AssayView import AssaySelectApi, AssayApi, PatientAssayApi
from pmsDoctor.views.ProtocolView import ProtocolApi, PatientProtocolApi
from pmsDoctor.views.AssayResultView import AssayResultApi
from pmsDoctor.views.DiagnosisView import DiagnosisApi
from pmsDoctor.views.MedicineView import MedicineDiagnosisApi

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
    path('assay-select-api/', AssaySelectApi.as_view(), name='assay-select-api'),
    path('assay-api/', AssayApi.as_view(), name='assay-api'),
    path('protocol-api/', ProtocolApi.as_view(), name='protocol-api'),
    path('assay-result-api/', AssayResultApi.as_view(), name='assay-result-api'),
    path('diagnosis-api/', DiagnosisApi.as_view(), name='diagnosis-api'),
    path('patient-assay-api/', PatientAssayApi.as_view(), name='patient-assay-api'),
    path('medicine-diagnosis-api/', MedicineDiagnosisApi.as_view(), name='medicine-diagnosis-api'),
    path('general-info-api/', DoctorGeneralInfoApi.as_view(), name='general-info-api'),
    path('contact-info-api/', DoctorContactInfoApi.as_view(), name='contact-info-api'),
    path('about-api/', DoctorAboutApi.as_view(), name='about-api'),
    path('education-type-api/', EducationTypeSelectApi.as_view(), name='education-type-api'),
    path('education-api/', DoctorEducationApi.as_view(), name='doctor-education-api'),
    path('prize-api/', DoctorPrizeApi.as_view(), name='doctor-prize-api'),
    path('article-api/', DoctorArticleApi.as_view(), name='article-api'),
    path('article-timeline-api/', DoctorArticleTimelineApi.as_view(), name='article-timeline-api'),
    path('media-api/', DoctorMediaApi.as_view(), name='media-api'),
    path('payment-api/', PaymentAccountApi.as_view(), name='media-api'),
    path('payment-discount-api/', PaymentAccountDiscountApi.as_view(), name='payment-discount-api'),
    path('payment-type-select-api/', PaymentTypeSelectApi.as_view(), name='payment-type-select-api'),
    path('checking-account-api/', PatientCheckingAccountApi.as_view(), name='checking-account-api'),
    path('payment-movement-api/', PaymentMovementApi.as_view(), name='payment-movement-api'),
    path('total-checking-account-api/', TotalCheckingAccountApi.as_view(), name='total-checking-account-api'),
    path('momentary-checking-account-api/', MomentaryCheckingAccountApi.as_view(),
         name='momentary-checking-account-api'),
    path('all-checking-account-api/', AllCheckingAccountApi.as_view(),
         name='all-checking-account-api'),
    path('blog-api/', BlogApi.as_view(), name='blog-api'),
    path('all-movement-api/', AllMomentaryCheckingAccountApi.as_view(), name='all-movement-api'),
    path('clinic-general-info-api/', ClinicGeneralInfoApi.as_view(), name='clinic-general-info-api'),
    path('clinic-media-api/', ClinicMediaApi.as_view(), name='clinic-media-api'),
    path('doctor-profile-api/', DoctorProfileApi.as_view(), name='dcotor-profile-api'),
    path('publish-blog-api/', PublishBlogApi.as_view(), name='publish-blog-api'),
    path('sponsored-blog-api/', SponsoredBlogApi.as_view(), name='sponsored-blog-api'),
    path('clinics-doctors-api/', ClinicsDoctorsApi.as_view(), name='clinics-doctors-api'),
    path('patient-profile-api/', PatientProfileApi.as_view(), name='patient-profile-api'),
    path('patient-protocol-api/', PatientProtocolApi.as_view(), name='patient-protocol-api'),
]
