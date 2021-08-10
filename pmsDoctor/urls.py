from django.urls import path

from pmsDoctor.views.DepartmentView import DepartmentSelectApi
from pmsDoctor.views.DoctorView import DoctorApi, DoctorSelectApi, DoctorGeneralInfoApi, DoctorContactInfoApi, \
    DoctorAboutApi, EducationTypeSelectApi, DoctorEducationApi, DoctorPrizeApi
from pmsDoctor.views.SecretaryView import SecretaryApi
from pmsDoctor.views.GenderView import GenderSelectApi
from pmsDoctor.views.PatientView import PatientApi, PatientSelectApi
from pmsDoctor.views.BloodGroupView import BloodGroupSelectApi
from pmsDoctor.views.AppointmentView import AppointmentApi, AppointmentCalendarApi
from pmsDoctor.views.AssayView import AssaySelectApi, AssayApi, PatientAssayApi
from pmsDoctor.views.ProtocolView import ProtocolApi
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
    path('doctor-education-api/', DoctorEducationApi.as_view(), name='doctor-education-api'),
    path('doctor-prize-api/', DoctorPrizeApi.as_view(), name='doctor-prize-api'),

]
