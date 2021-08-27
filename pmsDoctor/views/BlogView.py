# oxit staff view
import traceback

from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

from management.models.APIObject import APIObject
from pms.models import Blog
from pms.models.Assay import Assay
from pms.models.ProtocolAssay import ProtocolAssay
from pms.models.SelectObject import SelectObject
from pmsDoctor.serializers.AssaySerializer import AssaySerializer, AssayPageableSerializer
from pmsDoctor.serializers.BlogSerializer import BlogSerializer, BlogPageSerializer
from pmsDoctor.serializers.GeneralSerializer import SelectSerializer


class BlogApi(APIView):
    def get(self, request, format=None):
        try:
            if request.GET.get('id') is not None:
                blog = Blog.objects.get(uuid=request.GET.get('id'))
                api_object = dict()
                api_object['uuid'] = blog.uuid
                api_object['description'] = blog.description
                api_object['image'] = blog.image
                api_object['keyword'] = blog.keyword
                api_object['isPublish'] = blog.isPublish
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

                data = Blog.objects.filter(doctor__user=request.user, isDeleted=False).order_by('-id')[
                       lim_start:lim_end]
                count = Blog.objects.filter(doctor__user=request.user, isDeleted=False).count()
                arr = []

                for blog in data:
                    api_object = dict()
                    api_object['uuid'] = blog.uuid
                    api_object['description'] = blog.description
                    api_object['image'] = blog.image
                    api_object['keyword'] = blog.keyword
                    api_object['isPublish'] = blog.isPublish
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

    def post(self, request, format=None):
        serializer = BlogSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "blog is created"}, status=status.HTTP_200_OK)
        else:
            errors = dict()
            for key, value in serializer.errors.items():
                if key == 'departmentId':
                    errors['departmentId'] = value
                elif key == 'image':
                    errors['image'] = value
                elif key == 'keyword':
                    errors['keyword'] = value
                elif key == 'isPublish':
                    errors['isPublish'] = value
                elif key == 'description':
                    errors['description'] = value
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, format=None):
        try:
            instance = Blog.objects.get(uuid=request.GET.get('id'))
            serializer = BlogSerializer(data=request.data, instance=instance, context={'request': request})
            if serializer.is_valid():
                serializer.save()
                return Response({'message': "assay is updated"}, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception:
            traceback.print_exc()
            return Response(status.HTTP_400_BAD_REQUEST)

    def delete(self, request, format=None):
        try:
            blog = Blog.objects.get(uuid=request.GET.get('id'))
            blog.isDeleted = True
            blog.save()
            return Response('delete is success', status.HTTP_200_OK)
        except:
            traceback.print_exc()
            return Response(status.HTTP_400_BAD_REQUEST)
