from rest_framework import serializers


class MedicineSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    name = serializers.CharField()

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass
