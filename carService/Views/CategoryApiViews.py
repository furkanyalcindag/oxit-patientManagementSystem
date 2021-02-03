from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from carService.models import Category
from carService.models.CategoryObject import CategoryObject
from carService.models.CategorySelectObject import CategorySelectObject
from carService.serializers.CategorySerializer import CategorySerializer, CategorySelectSerializer
from carService.services import CategoryServices


class CategoryApi(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        if request.GET.get('id') is None:
            categories = Category.objects.all()
            category_objects = []
            for category in categories:
                category_object = CategoryObject()
                category_object.name = category.name
                category_object.id = category.id
                category_object.parentPath = CategoryServices.get_category_path(category, '')
                category_objects.append(category_object)

            serializer = CategorySerializer(category_objects, many=True, context={'request': request})
            return Response(serializer.data, status.HTTP_200_OK)
        else:
            category_object = CategoryObject()
            category = Category.objects.get(id=int(request.GET.get('id')))
            category_object.name = category.name
            category_object.id = category.id
            if category.parent:
                category_object.parent = category.parent.id
            else:
                category_object.parent=0
            category_object.parentPath = CategoryServices.get_category_path(category, '')
            serializer = CategorySerializer(category_object, context={'request': request})
            return Response(serializer.data, status.HTTP_200_OK)

    def post(self, request, format=None):
        serializer = CategorySerializer(data=request.data, context={'request': request})

        if serializer.is_valid():
            serializer.save()
            return Response({"message": "category is created"}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, format=None):
        instance = Category.objects.get(id=request.GET.get('id'))
        serializer = CategorySerializer(data=request.data
                                        , instance=instance, context={'request': request})

        if serializer.is_valid():
            serializer.save()
            return Response({"message": "brand is updated"}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CategorySelectApi(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        categories = Category.objects.all()
        category_objects = []
        category_objectRoot = CategorySelectObject()
        category_objectRoot.label = "Yok"
        category_objectRoot.value = "0"
        category_objects.append(category_objectRoot)
        for category in categories:
            path = CategoryServices.get_category_arr(category, [])
            category_object = CategorySelectObject()
            category_object.value = category.id
            category_object.label = CategoryServices.get_path_from_arr(path)
            category_objects.append(category_object)

        serializer = CategorySelectSerializer(category_objects, many=True, context={'request': request})
        return Response(serializer.data, status.HTTP_200_OK)
