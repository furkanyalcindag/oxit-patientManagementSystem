from django.contrib.auth.models import User
from django.db import models

from pms.models.BaseModel import BaseModel


class Profile(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profileImage = models.TextField(null=True, blank=True)
    mobilePhone = models.CharField(max_length=20, null=True, blank=True)
    city = models.CharField(max_length=64, blank=True, null=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    isSendMail = models.BooleanField(default=False)
    isSendNotification = models.BooleanField(default=True)
    isAcceptUserPrivacyContract = models.BooleanField(default=False)
    deviceOSType = models.CharField(max_length=128)
    deviceId = models.CharField(max_length=256)
    identityNumber = models.CharField(max_length=256, null=False)
    website = models.CharField(max_length=256)
    instagram = models.CharField(max_length=256)
    facebook = models.CharField(max_length=256)
    youtube = models.CharField(max_length=256)
    linkedin = models.CharField(max_length=256)
