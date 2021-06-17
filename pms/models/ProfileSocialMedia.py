from django.db import models
from drf_api_logger.models import BaseModel

from pms.models.SocialMedia import SocialMedia
from pms.models.Profile import Profile


class ProfileSocialMedia(BaseModel):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    socialMedia = models.ForeignKey(SocialMedia, on_delete=models.CASCADE)
    link = models.CharField(max_length=256, null=True, blank=True)
