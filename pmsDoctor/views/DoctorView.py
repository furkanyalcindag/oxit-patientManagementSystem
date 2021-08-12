# oxit doctor view
import traceback

from django.http import JsonResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from management.serializers.GeneralSerializer import SelectSerializer
from pms.models.Media import Media
from pms.models.Prize import Prize
from pms.models.Profile import Profile
from pms.models.DoctorArticle import DoctorArticle

from pms.models.DoctorEducation import DoctorEducation
from pms.models.EducationType import EducationType
from pms.models.SelectObject import SelectObject
from pms.models.Staff import Staff
from pmsDoctor.models.APIObject import APIObject
from pmsDoctor.serializers.DoctorSerializer import DoctorPageSerializer, DoctorSerializer, DoctorGeneralInfoSerializer, \
    DoctorContactInfoSerializer, DoctorAboutSerializer, DoctorEducationSerializer, DoctorEducationPageSerializer, \
    DoctorPrizeSerializer, DoctorArticleSerializer, DoctorMediaSerializer


class DoctorApi(APIView):
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
                count = 10

                name = ''
                if request.GET.get('page') is not None:
                    active_page = int(request.GET.get('page'))
                if request.GET.get('name') is not None:
                    name = request.GET.get('name')
                if request.GET.get('count') is not None:
                    count = int(request.GET.get('count'))

                lim_start = count * (int(active_page) - 1)
                lim_end = lim_start + int(count)

                data = Staff.objects.filter(profile__user__first_name__icontains=name, isDeleted=False).order_by('-id')[
                       lim_start:lim_end]
                filtered_count = Staff.objects.filter(profile__user__first_name__icontains=name,
                                                      isDeleted=False).count()
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
                api_object.recordsFiltered = filtered_count
                api_object.recordsTotal = Staff.objects.filter(isDeleted=False).count()
                serializer = DoctorPageSerializer(api_object, context={'request': request})
                return Response(serializer.data, status.HTTP_200_OK)

        except Exception as e:
            traceback.print_exc()
            return Response("", status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request, format=None):
        serializer = DoctorSerializer(data=request.data, context={'request', request})
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "prize is created"}, status=status.HTTP_200_OK)
        else:
            errors = dict()
            for key, value in serializer.errors.items():
                if key == 'firstName':
                    errors['isim'] = value
                elif key == 'lastName':
                    errors['soyisim'] = value
                elif key == 'email':
                    errors['mail'] = value
                elif key == 'departmentId':
                    errors['departmentId'] = value
                elif key == 'insuranceNumber':
                    errors['insuranceNumber'] = value
                elif key == 'diplomaNo':
                    errors['diplomaNo'] = value
                elif key == 'title':
                    errors['title'] = value
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, format=None):
        try:
            instance = Staff.objects.get(uuid=request.GET.get('id'))
            serializer = DoctorSerializer(data=request.data, instance=instance, context={'request': request})
            if serializer.is_valid():
                serializer.save()
                return Response({'message': "staff is updated"}, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception:
            traceback.print_exc()
            return Response(status.HTTP_400_BAD_REQUEST)

    def delete(self, request, format=None):
        try:
            staff = Staff.objects.get(uuid=request.GET.get('id'))
            staff.isDeleted = True
            staff.save()
            return Response('delete is success', status.HTTP_200_OK)
        except:
            traceback.print_exc()
            return Response(status.HTTP_400_BAD_REQUEST)


class DoctorSelectApi(APIView):
    def get(self, request, format=None):
        try:
            select_arr = []
            data = Staff.objects.filter(isDeleted=False)

            for doctor in data:
                select_object = SelectObject()
                select_object.value = doctor.profile.user.id
                select_object.label = doctor.profile.user.first_name + ' ' + doctor.profile.user.last_name
                select_arr.append(select_object)

            serializer = SelectSerializer(select_arr, many=True, context={'request': request})

            return Response(serializer.data, status.HTTP_200_OK)
        except Exception as e:
            return Response("error", status.HTTP_500_INTERNAL_SERVER_ERROR)


class DoctorGeneralInfoApi(APIView):
    def get(self, request, format=None):
        try:
            staff = Staff.objects.get(profile__user=request.user)
            api_data = dict()
            api_data['firstName'] = staff.profile.user.first_name
            api_data['lastName'] = staff.profile.user.last_name
            api_data['profileImage'] = staff.profile.profileImage
            api_data['diplomaNo'] = staff.diplomaNo
            api_data['profession'] = staff.profession
            api_data['title'] = staff.title
            api_department_data = dict()
            api_department_data['label'] = staff.department.name
            api_department_data['value'] = staff.department.id
            api_data['department'] = api_department_data

            serializer = DoctorGeneralInfoSerializer(api_data, context={'request': request})

            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            traceback.print_exc()
            return Response(str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request, format=None):
        try:
            instance = Staff.objects.get(profile__user=request.user)
            serializer = DoctorGeneralInfoSerializer(data=request.data, instance=instance,
                                                     context={'request': request})
            if serializer.is_valid():
                serializer.save()
                return Response({"message": "doctor information is updated"}, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except:
            traceback.print_exc()
            return Response('error', status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class DoctorContactInfoApi(APIView):
    def get(self, request, format=None):
        try:
            profile = Profile.objects.get(user=request.user)
            api_data = dict()
            api_data['address'] = profile.address
            api_data['website'] = profile.website
            api_data['mobilePhone'] = profile.mobilePhone
            api_data['instagram'] = profile.instagram
            api_data['facebook'] = profile.facebook
            api_data['youtube'] = profile.youtube
            api_data['linkedin'] = profile.linkedin
            api_data['email'] = profile.user.email

            serializer = DoctorContactInfoSerializer(api_data, context={'request': request})

            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            traceback.print_exc()
            return Response(str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request, format=None):
        try:
            instance = Profile.objects.get(user=request.user)
            serializer = DoctorContactInfoSerializer(data=request.data, instance=instance,
                                                     context={'request': request})
            if serializer.is_valid():
                serializer.save()
                return Response({"message": "doctor information is updated"}, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except:
            traceback.print_exc()
            return Response('error', status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class DoctorAboutApi(APIView):
    def get(self, request, format=None):
        try:
            staff = Staff.objects.get(profile__user=request.user)
            api_data = dict()
            api_data['about'] = staff.about

            serializer = DoctorAboutSerializer(api_data, context={'request': request})

            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            traceback.print_exc()
            return Response(str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request, format=None):
        try:
            instance = Staff.objects.get(profile__user=request.user)
            serializer = DoctorAboutSerializer(data=request.data, instance=instance,
                                               context={'request': request})
            if serializer.is_valid():
                serializer.save()
                return Response({"message": "doctor information is updated"}, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except:
            traceback.print_exc()
            return Response('error', status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, format=None):
        try:
            staff = Staff.objects.get(uuid=request.GET.get('id'))
            staff.about = ''
            staff.save()
            return Response('delete is success', status.HTTP_200_OK)
        except:
            traceback.print_exc()
            return Response(status.HTTP_400_BAD_REQUEST)


class DoctorEducationApi(APIView):
    def get(self, request, format=None):
        try:
            if request.GET.get('id') is not None:
                education = DoctorEducation.objects.get(uuid=request.GET.get('id'))
                api_object = dict()
                api_object['uuid'] = education.uuid
                api_object['universityName'] = education.universityName
                api_object['facultyName'] = education.facultyName
                api_object['departmentName'] = education.departmentName
                api_type_data = dict()
                api_type_data['label'] = education.educationType.name
                api_type_data['value'] = education.educationType.id

                api_object['educationType'] = api_type_data

                serializer = DoctorEducationSerializer(api_object, context={'request': request})
                return Response(serializer.data, status.HTTP_200_OK)

            else:
                data = DoctorEducation.objects.filter(isDeleted=False).order_by('-id')
                filtered_count = DoctorEducation.objects.filter(isDeleted=False).count()
                arr = []

                for education in data:
                    api_object = dict()
                    api_object['uuid'] = education.uuid
                    api_object['universityName'] = education.universityName
                    api_object['facultyName'] = education.facultyName
                    api_object['departmentName'] = education.departmentName
                    api_type_data = dict()
                    api_type_data['label'] = education.educationType.name
                    api_type_data['value'] = education.educationType.id

                    api_object['educationType'] = api_type_data
                    arr.append(api_object)
                api_object = APIObject()
                api_object.data = arr
                api_object.recordsFiltered = filtered_count
                api_object.recordsTotal = DoctorEducation.objects.filter(isDeleted=False).count()
                serializer = DoctorEducationPageSerializer(api_object, context={'request': request})
                return Response(serializer.data, status.HTTP_200_OK)

        except Exception as e:
            traceback.print_exc()
            return Response("", status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request, format=None):
        serializer = DoctorEducationSerializer(data=request.data, context={'request', request})
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Doctor is created"}, status=status.HTTP_200_OK)
        else:
            errors = dict()
            for key, value in serializer.errors.items():
                if key == 'universityName':
                    errors['universityName'] = value
                elif key == 'facultyName':
                    errors['facultyName'] = value
                elif key == 'departmentName':
                    errors['departmentName'] = value
                elif key == 'educationType':
                    errors['educationType'] = value
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, format=None):
        try:
            instance = DoctorEducation.objects.get(uuid=request.GET.get('id'))
            serializer = DoctorEducationSerializer(data=request.data, instance=instance, context={'request': request})
            if serializer.is_valid():
                serializer.save()
                return Response({'message': "staff is updated"}, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception:
            traceback.print_exc()
            return Response(status.HTTP_400_BAD_REQUEST)

    def delete(self, request, format=None):
        try:
            education = DoctorEducation.objects.get(uuid=request.GET.get('id'))
            education.isDeleted = True
            education.save()
            return Response('delete is success', status.HTTP_200_OK)
        except:
            traceback.print_exc()
            return Response(status.HTTP_400_BAD_REQUEST)


class EducationTypeSelectApi(APIView):
    def get(self, request, format=None):
        try:
            select_arr = []
            data = EducationType.objects.all()

            for type in data:
                select_object = SelectObject()
                select_object.value = type.id
                select_object.label = type.name
                select_arr.append(select_object)

            serializer = SelectSerializer(select_arr, many=True, context={'request': request})

            return Response(serializer.data, status.HTTP_200_OK)
        except Exception as e:
            return Response("error", status.HTTP_500_INTERNAL_SERVER_ERROR)


class DoctorPrizeApi(APIView):

    def get(self, request, format=None):

        try:
            if request.GET.get('id') is not None:
                prize = Prize.objects.get(doctor__profile__user=request.user,
                                          uuid=request.GET.get('id'))

                api_data = dict()

                api_data['uuid'] = prize.uuid
                api_data['title'] = prize.title
                api_data['description'] = prize.description
                api_data['date'] = prize.date
                api_data['image'] = prize.image

                serializer = DoctorPrizeSerializer(api_data, context={'request': request})
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:

                prizes = Prize.objects.filter(doctor__profile__user=request.user,
                                              isDeleted=False)
                arr = []
                for prize in prizes:
                    api_data = dict()

                    api_data['uuid'] = prize.uuid
                    api_data['title'] = prize.title
                    api_data['description'] = prize.description
                    api_data['image'] = prize.image
                    api_data['date'] = prize.date

                    arr.append(api_data)

                serializer = DoctorPrizeSerializer(arr, many=True, context={'request': request})
                return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            traceback.print_exc()
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, format=None):
        try:
            instance = Prize.objects.get(doctor__profile__user=request.user,
                                         uuid=request.GET.get('id'))
            serializer = DoctorPrizeSerializer(data=request.data, instance=instance, context={'request': request})
            if serializer.is_valid():
                serializer.save()
                return Response({"message": "prize is updated"}, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except:
            traceback.print_exc()
            return Response("error", status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request, format=None):
        serializer = DoctorPrizeSerializer(data=request.data, context={'request': request})

        if serializer.is_valid():
            serializer.save()
            return Response({"message": "prize is created"}, status=status.HTTP_200_OK)
        else:
            errors_dict = dict()
            for key, value in serializer.errors.items():
                if key == 'title':
                    errors_dict['title'] = value

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, format=None):
        try:
            prize = Prize.objects.get(uuid=request.GET.get('id'),
                                      doctor__profile__user=request.user)
            prize.isDeleted = True
            prize.save()

            return Response(status=status.HTTP_200_OK)
        except Exception:
            traceback.print_exc()
            return Response(status=status.HTTP_400_BAD_REQUEST)


class DoctorArticleApi(APIView):

    def get(self, request, format=None):

        try:
            if request.GET.get('id') is not None:
                article = DoctorArticle.objects.get(doctor__profile__user=request.user,
                                                    uuid=request.GET.get('id'))

                api_data = dict()

                api_data['uuid'] = article.uuid
                api_data['title'] = article.title
                api_data['link'] = article.link
                api_data['date'] = article.date

                serializer = DoctorArticleSerializer(api_data, context={'request': request})
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:

                articles = DoctorArticle.objects.filter(doctor__profile__user=request.user,
                                                        isDeleted=False)
                arr = []
                for article in articles:
                    api_data = dict()

                    api_data['uuid'] = article.uuid
                    api_data['title'] = article.title
                    api_data['link'] = article.link
                    api_data['date'] = article.date

                    arr.append(api_data)

                serializer = DoctorArticleSerializer(arr, many=True, context={'request': request})
                return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            traceback.print_exc()
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, format=None):
        try:
            instance = DoctorArticle.objects.get(doctor__profile__user=request.user,
                                                 uuid=request.GET.get('id'))
            serializer = DoctorArticleSerializer(data=request.data, instance=instance, context={'request': request})
            if serializer.is_valid():
                serializer.save()
                return Response({"message": "prize is updated"}, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except:
            traceback.print_exc()
            return Response("error", status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request, format=None):
        serializer = DoctorArticleSerializer(data=request.data, context={'request': request})

        if serializer.is_valid():
            serializer.save()
            return Response({"message": "prize is created"}, status=status.HTTP_200_OK)
        else:
            errors_dict = dict()
            for key, value in serializer.errors.items():
                if key == 'title':
                    errors_dict['title'] = value

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, format=None):
        try:
            article = DoctorArticle.objects.get(uuid=request.GET.get('id'),
                                                doctor__profile__user=request.user)
            article.isDeleted = True
            article.save()

            return Response(status=status.HTTP_200_OK)
        except Exception:
            traceback.print_exc()
            return Response(status=status.HTTP_400_BAD_REQUEST)


class DoctorArticleTimelineApi(APIView):

    def get(self, request, format=None):

        try:
            articles = DoctorArticle.objects.filter(doctor__profile__user=request.user,
                                                    isDeleted=False).order_by('date')
            year_arr = []
            dict_by_year = dict()
            for article in articles:
                if article.date.year not in year_arr:
                    year_arr.append(str(article.date.year))
            for year in year_arr:
                articles_arr = []
                year_articles = DoctorArticle.objects.filter(doctor__profile__user=request.user,
                                                             isDeleted=False, date__year=year).order_by('-date')
                for art in year_articles:
                    record = {"title": art.title, "date": art.date}
                    articles_arr.append(record)
                dict_by_year[str(year)] = articles_arr
            return Response(dict_by_year, status=status.HTTP_200_OK)
        except Exception as e:
            traceback.print_exc()
            return Response(status=status.HTTP_400_BAD_REQUEST)


class DoctorMediaApi(APIView):

    def get(self, request, format=None):

        try:
            medias = Media.objects.filter(doctor__profile__user=request.user,
                                          isDeleted=False)
            arr = []
            for media in medias:
                api_data = dict()

                api_data['uuid'] = media.uuid
                api_data['media'] = media.media

                arr.append(api_data)

            serializer = DoctorMediaSerializer(arr, many=True, context={'request': request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            traceback.print_exc()
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, format=None):
        serializer = DoctorMediaSerializer(data=request.data, context={'request': request})

        if serializer.is_valid():
            serializer.save()
            return Response({"message": "media is created"}, status=status.HTTP_200_OK)
        else:
            errors_dict = dict()
            for key, value in serializer.errors.items():
                if key == 'media':
                    errors_dict['media'] = value

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, format=None):
        try:
            media = Media.objects.get(uuid=request.GET.get('id'),
                                      doctor__profile__user=request.user)
            media.isDeleted = True
            media.save()

            return Response(status=status.HTTP_200_OK)
        except Exception:
            traceback.print_exc()
            return Response(status=status.HTTP_400_BAD_REQUEST)
