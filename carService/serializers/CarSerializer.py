from rest_framework import serializers

from carService.models import Profile, Car


class CarSerializer(serializers.Serializer):
    uuid = serializers.UUIDField(read_only=True)
    plate = serializers.CharField(required=True)
    brand = serializers.CharField(required=True)
    model = serializers.CharField(required=True)
    year = serializers.IntegerField(required=True)
    engine = serializers.CharField(required=True)
    profileUuid = serializers.UUIDField(write_only=True)
    oilType = serializers.CharField(required=True)
    chassisNumber = serializers.CharField(required=True)
    currentKM = serializers.CharField(required=True)
    engineNumber = serializers.CharField(required=True)
    color = serializers.CharField(required=True)

    def create(self, validated_data):
        try:
            profile = Profile.objects.get(uuid=validated_data.get('profileUuid'))
            if profile:
                car = Car()
                car.brand = validated_data.get('brand')
                car.color = validated_data.get('color')
                car.currentKM = validated_data.get('currentKM')
                car.chassisNumber = validated_data.get('chassisNumber')
                car.profile = profile
                car.model = validated_data.get('model')
                car.year = validated_data.get('year')
                car.engine = validated_data.get('engine')
                car.oilType = validated_data.get('oilType')
                car.engineNumber = validated_data.get('engineNumber')
                car.plate = validated_data.get('plate')
            return profile
        except Exception:

            raise serializers.ValidationError("lütfen tekrar deneyiniz")
