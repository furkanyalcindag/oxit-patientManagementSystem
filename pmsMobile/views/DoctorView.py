# oxit doctor view
import traceback
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from pms.models.Prize import Prize
from pms.models.DoctorArticle import DoctorArticle

from pms.models.DoctorEducation import DoctorEducation
from pms.models.Staff import Staff
from pmsDoctor.models.APIObject import APIObject
from pmsDoctor.serializers.DoctorSerializer import DoctorPageSerializer, DoctorSerializer


class DoctorProfileApi(APIView):
    def get(self, request, format=None):
        try:
            doctor = Staff.objects.get(uuid=request.GET.get('id'))
            general_info = dict()
            general_info['firstName'] = doctor.profile.user.first_name
            general_info['lastName'] = doctor.profile.user.last_name
            general_info['profileImage'] = doctor.profile.profileImage
            general_info['diplomaNo'] = doctor.diplomaNo
            general_info['profession'] = doctor.profession
            general_info['title'] = doctor.title
            api_department_data = dict()
            api_department_data['label'] = doctor.department.name
            api_department_data['value'] = doctor.department.id
            general_info['department'] = api_department_data
            about = doctor.about
            educations = DoctorEducation.objects.filter(doctor__uuid=request.GET.get('id'))
            educations_array = []
            for education in educations:
                data = dict()
                data['universityName'] = education.universityName
                data['facultyName'] = education.facultyName
                data['departmentName'] = education.departmentName
                data['educationType'] = education.educationType
                educations_array.append(data)
            articles = DoctorArticle.objects.filter(doctor__uuid=request.GET.get('id'))
            articles_array = []
            for article in articles:
                data = dict()
                data['date'] = article.date
                data['link'] = article.link
                data['title'] = article.title
                articles_array.append(data)
            prizes = Prize.objects.filter(doctor__uuid=request.GET.get('id'))
            prizes_array = []
            for prize in prizes:
                data = dict()
                data['title'] = prize.title
                data['description'] = prize.description
                data['date'] = prize.date
                data['image'] = prize.image
                prizes_array.append(data)
            doctor = Staff.objects.get(uuid=request.GET.get('id'))
            contact_info = dict()
            contact_info['address'] = doctor.profile.address
            contact_info['website'] = doctor.profile.website
            contact_info['mobilePhone'] = doctor.profile.mobilePhone
            contact_info['instagram'] = doctor.profile.instagram
            contact_info['facebook'] = doctor.profile.facebook
            contact_info['youtube'] = doctor.profile.youtube
            contact_info['linkedin'] = doctor.profile.linkedin
            contact_info['email'] = doctor.profile.user.email

            api_data = dict()
            api_data['generalInfo'] = general_info
            api_data['contactInfo'] = contact_info
            api_data['prizes'] = prizes_array
            api_data['educations'] = educations_array
            api_data['articles'] = articles_array
            api_data['about'] = about

            return Response(api_data, status.HTTP_200_OK)

        except:
            traceback.print_exc()
            return Response('error', status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ClinicsDoctorsApi(APIView):
    def get(self, request, format=None):
        try:
            if request.GET.get('id') is not None:
                staff = Staff.objects.get(uuid=request.GET.get('id'))
                api_object = dict()
                api_object['uuid'] = staff.uuid
                api_object['firstName'] = staff.profile.user.first_name
                api_object['lastName'] = staff.profile.user.last_name
                api_object['email'] = staff.profile.user.email
                api_object['diplomaNo'] = staff.diplomaNo
                api_object['insuranceNumber'] = staff.insuranceNumber
                api_object['title'] = staff.title
                api_department_data = dict()
                api_department_data['label'] = staff.department.name
                api_department_data['value'] = staff.department.id

                api_object['department'] = api_department_data

                serializer = DoctorSerializer(api_object, context={'request': request})
                return Response(serializer.data, status.HTTP_200_OK)

            else:
                active_page = 1
                count = 0
                name = ''

                if request.GET.get('activePage') is not None:
                    active_page = int(request.GET.get('activePage'))

                lim_start = 10 * (int(active_page) - 1)
                lim_end = lim_start + 10

                data = Staff.objects.filter(clinic__uuid=request.GET.get('clinicId'),
                                            isDeleted=False).order_by('-id')[
                       lim_start:lim_end]
                count = Staff.objects.filter(clinic__uuid=request.GET.get('clinicId'), isDeleted=False).count()
                arr = []

                for staff in data:
                    api_object = dict()
                    api_object['uuid'] = staff.uuid
                    api_object['firstName'] = staff.profile.user.first_name
                    api_object['lastName'] = staff.profile.user.last_name
                    api_object['diplomaNo'] = staff.diplomaNo
                    api_object['insuranceNumber'] = staff.insuranceNumber
                    api_object['title'] = staff.title
                    api_object['email'] = staff.profile.user.email
                    api_department_data = dict()
                    api_department_data['label'] = staff.department.name
                    api_department_data['value'] = staff.department.id
                    api_object['department'] = api_department_data
                    arr.append(api_object)
                api_object = APIObject()
                api_object.data = arr
                api_object.recordsFiltered = data.count()
                api_object.recordsTotal = count
                if count % 10 == 0:
                    api_object.activePage = count / 10
                else:
                    api_object.activePage = (count / 10) + 1
                serializer = DoctorPageSerializer(api_object, context={'request': request})
                return Response(serializer.data, status.HTTP_200_OK)

        except Exception as e:
            traceback.print_exc()
            return Response("", status.HTTP_500_INTERNAL_SERVER_ERROR)
