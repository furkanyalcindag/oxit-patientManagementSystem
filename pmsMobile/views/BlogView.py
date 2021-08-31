# oxit staff view
import traceback

from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

from management.models.APIObject import APIObject
from pms.models import Blog
from pmsDoctor.serializers.BlogSerializer import BlogSerializer, BlogPageSerializer


class PublishBlogApi(APIView):
    def get(self, request, format=None):
        try:
            if request.GET.get('id') is not None:
                blog = Blog.objects.get(uuid=request.GET.get('id'))
                api_object = dict()
                api_object['uuid'] = blog.uuid
                api_object['description'] = blog.description
                api_object['image'] = blog.image
                api_object['title'] = blog.title
                api_object['keyword'] = blog.keyword
                api_object['isPublish'] = blog.isPublish
                api_object['isSponsored'] = blog.isSponsored
                api_department_data = dict()
                api_department_data[
                    'label'] = blog.department.name
                api_department_data['value'] = blog.department.id
                api_object['department'] = api_department_data
                serializer = BlogSerializer(api_object, context={'request': request})
                return Response(serializer.data, status.HTTP_200_OK)

            else:
                active_page = 1
                count = 0

                name = ''
                if request.GET.get('activePage') is not None:
                    active_page = int(request.GET.get('activePage'))

                lim_start = 10 * (int(active_page) - 1)
                lim_end = lim_start + 10

                data = Blog.objects.filter(isPublish=True, isSponsored=False, isDeleted=False).order_by('-id')[
                       lim_start:lim_end]
                count = Blog.objects.filter(isPublish=True, isSponsored=False, isDeleted=False).count()
                arr = []

                for blog in data:
                    api_object = dict()
                    api_object['uuid'] = blog.uuid
                    api_object['description'] = blog.description
                    api_object['title'] = blog.title
                    api_object['image'] = blog.image
                    api_object['keyword'] = blog.keyword
                    api_object['isPublish'] = blog.isPublish
                    api_object['isSponsored'] = blog.isSponsored
                    api_department_data = dict()
                    api_department_data[
                        'label'] = blog.department.name
                    api_department_data['value'] = blog.department.id
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
                serializer = BlogPageSerializer(api_object, context={'request': request})
                return Response(serializer.data, status.HTTP_200_OK)

        except Exception as e:
            traceback.print_exc()
            return Response("", status.HTTP_500_INTERNAL_SERVER_ERROR)


class SponsoredBlogApi(APIView):
    def get(self, request, format=None):
        try:
            if request.GET.get('id') is not None:
                blog = Blog.objects.get(uuid=request.GET.get('id'))
                api_object = dict()
                api_object['uuid'] = blog.uuid
                api_object['description'] = blog.description
                api_object['image'] = blog.image
                api_object['title'] = blog.title
                api_object['keyword'] = blog.keyword
                api_object['isPublish'] = blog.isPublish
                api_object['isSponsored'] = blog.isSponsored
                api_department_data = dict()
                api_department_data[
                    'label'] = blog.department.name
                api_department_data['value'] = blog.department.id
                api_object['department'] = api_department_data
                serializer = BlogSerializer(api_object, context={'request': request})
                return Response(serializer.data, status.HTTP_200_OK)

            else:
                active_page = 1
                count = 0

                name = ''
                if request.GET.get('activePage') is not None:
                    active_page = int(request.GET.get('activePage'))

                lim_start = 10 * (int(active_page) - 1)
                lim_end = lim_start + 10

                data = Blog.objects.filter(isPublish=True, isSponsored=True, isDeleted=False).order_by('-id')[
                       lim_start:lim_end]
                count = Blog.objects.filter(isPublish=True, isSponsored=True, isDeleted=False).count()
                arr = []

                for blog in data:
                    api_object = dict()
                    api_object['uuid'] = blog.uuid
                    api_object['description'] = blog.description
                    api_object['title'] = blog.title
                    api_object['image'] = blog.image
                    api_object['keyword'] = blog.keyword
                    api_object['isPublish'] = blog.isPublish
                    api_object['isSponsored'] = blog.isSponsored
                    api_department_data = dict()
                    api_department_data[
                        'label'] = blog.department.name
                    api_department_data['value'] = blog.department.id
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
                serializer = BlogPageSerializer(api_object, context={'request': request})
                return Response(serializer.data, status.HTTP_200_OK)

        except Exception as e:
            traceback.print_exc()
            return Response("", status.HTTP_500_INTERNAL_SERVER_ERROR)
