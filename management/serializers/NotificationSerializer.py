import traceback

from django.db import transaction
from rest_framework import serializers
from pms.models.Notification import Notification


class NotificationSerializer(serializers.Serializer):

    title = serializers.CharField(required=True)
    body = serializers.CharField(required=True)
    image = serializers.CharField(required=True)
    link = serializers.CharField(required=True)

    def update(self, instance, validated_data):
        pass


    def create(self, validated_data):
        try:
            with transaction.atomic():
                notification = Notification()
                notification.title = validated_data.get('title')
                notification.body = validated_data.get('body')
                notification.image = validated_data.get('image')
                notification.link = validated_data.get('link')
                notification.save()
                return notification

        except Exception as e:
            traceback.print_exc()
            raise serializers.ValidationError("lütfen tekrar deneyiniz")
