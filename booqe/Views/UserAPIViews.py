# kullanıcı oluşturma
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from booqe.models import Profile
from booqe.models.PinnedBlog import PinnedBlog
from booqe.models.ProfileObject import ProfileObjectForFlutter
from booqe.serializers.UserSerializer import UserRegisterOrGetSerializer, ProfileSerializerFlutter, \
    NotificationSerializerFlutter, PasswordSerializer, ProfilePhotoSerializer


class CreateUserMember(APIView):

    def get(self, request, format=None):
        profiles = Profile.objects.all()
        serializer_context = {
            'request': request,
        }
        serializer = UserRegisterOrGetSerializer(profiles, many=True, context=serializer_context)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = UserRegisterOrGetSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User created"}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_405_METHOD_NOT_ALLOWED)


class ProfileInformation(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        array_profile = []

        profile = Profile.objects.get(user=request.user)

        pins = PinnedBlog.objects.filter(profile=profile)

       

        profile_object = ProfileObjectForFlutter(profileImage=profile.profileImage, pinCount=pins.count(),
                                                 username=request.user.username)

        profile_object.notification = profile.notification
        profile_object.email = request.user.email
        array_profile.append(profile_object)
        serializer_context = {
            'request': request,
        }
        serializer = ProfileSerializerFlutter(array_profile, many=True, context=serializer_context)

        return Response(serializer.data)


class NotificationApi(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, format=None):
        serializer = NotificationSerializerFlutter(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({"message": serializer.instance.notification}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_405_METHOD_NOT_ALLOWED)


# Şifre değişme
class ChangePassword(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, format=None):
        serializer = PasswordSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Password Changed"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ChangeProfileImage(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, format=None):
        serializer = ProfilePhotoSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Photo Changed"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
