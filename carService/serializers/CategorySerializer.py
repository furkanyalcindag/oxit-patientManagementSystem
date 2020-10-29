from rest_framework import serializers

from carService.models import Car, Category


class CategorySerializer(serializers.Serializer):
    name = serializers.CharField(required=True)
    parent = serializers.IntegerField(required=True, write_only=True, allow_null=True)
    parentPath = serializers.CharField(read_only=True)

    def create(self, validated_data):
        try:
            category = Category()
            category.name = validated_data.get('name')
            if validated_data.get('parent') != 0:
                parent_category = Category.objects.get(pk=validated_data.get('parent'))
                category.parent = parent_category

            category.save()
            return category

        except Exception:

            raise serializers.ValidationError("lütfen tekrar deneyiniz")

    def update(self, instance, validated_data):
        pass


class CategorySelectSerializer(serializers.Serializer):
    label = serializers.CharField()
    value = serializers.CharField()

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass
