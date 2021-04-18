from rest_framework import serializers




class PageSerializer(serializers.Serializer):

    recordsTotal = serializers.IntegerField()
    recordsFiltered = serializers.IntegerField()
    activePage = serializers.IntegerField()

