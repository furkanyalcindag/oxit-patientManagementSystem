from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from carService.models import Category
from carService.models.CategoryObject import CategoryObject
from carService.serializers.CategorySerializer import CategorySerializer
from carService.services import CategoryServices

from rest_framework.response import Response


class CategoryApi(APIView):
    # permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        categories = Category.objects.all()
        category_objects = []
        for category in categories:
            category_object = CategoryObject()
            category_object.name = category.name
            category_object.parentPath = CategoryServices.get_category_path(category, '')
            category_objects.append(category_object)

        serializer = CategorySerializer(category_objects, many=True, context={'request': request})
        return Response(serializer.data, status.HTTP_200_OK)

    def post(self, request, format=None):
        serializer = CategorySerializer(data=request.data, context={'request': request})

        if serializer.is_valid():
            serializer.save()
            return Response({"message": "category is created"}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
