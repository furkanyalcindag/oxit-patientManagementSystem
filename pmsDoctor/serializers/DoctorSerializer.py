import traceback

from django.contrib.auth.models import User, Group
from django.db import transaction
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from pms.models import Staff, Department, Profile, Prize
from pms.models.DoctorArticle import DoctorArticle
from pms.models.DoctorEducation import DoctorEducation
from pms.models.EducationType import EducationType
from pmsDoctor.serializers.GeneralSerializer import SelectSerializer, PageSerializer


class DoctorSerializer(serializers.Serializer):
    uuid = serializers.UUIDField(read_only=True)
    firstName = serializers.CharField()
    lastName = serializers.CharField()
    diplomaNo = serializers.CharField()
    insuranceNumber = serializers.CharField()
    title = serializers.CharField()
    departmentId = serializers.IntegerField(write_only=True)
    department = SelectSerializer(read_only=True)
    email = serializers.CharField()

    def update(self, instance, validated_data):
        user = instance.profile.user
        user.first_name = validated_data.get('firstName')
        user.last_name = validated_data.get('lastName')
        user.email = validated_data.get('email')
        user.username = validated_data.get('email')
        user.save()
        instance.diplomaNo = validated_data.get('diplomaNo')
        instance.insuranceNumber = validated_data.get('insuranceNumber')
        instance.title = validated_data.get('title')
        instance.department = Department.objects.get(id=validated_data.get('departmentId'))
        instance.save()

        return instance

    def create(self, validated_data):
        try:
            with transaction.atomic():
                user = User.objects.create_user(username=validated_data.get('email'),
                                                email=validated_data.get('email'))
                user.first_name = validated_data.get('firstName')
                user.last_name = validated_data.get('lastName')
                user.set_password('oxit2016')
                group = Group.objects.get(name='Doctor')
                user.groups.add(group)
                user.save()
                profile = Profile()
                profile.user = user
                profile.save()
                staff = Staff()
                staff.profile = profile
                staff.diplomaNo = validated_data.get('diplomaNo')
                staff.insuranceNumber = validated_data.get('insuranceNumber')
                staff.title = validated_data.get('title')
                staff.department = Department.objects.get(id=int(validated_data.get('departmentId')))
                staff.save()

                return staff
        except:
            traceback.print_exc()
            raise ValidationError("lütfen tekrar deneyiniz")

    def validate_email(self, email):

        user = None
        if self.instance is not None:

            user = Staff.objects.get(uuid=self.context['request'].query_params['id']).profile.user

            if User.objects.exclude(id=user.id).filter(username=email).count() > 0:
                raise serializers.ValidationError("Bu email sistemde kayıtlıdır")

        else:
            if User.objects.filter(username=email).count() > 0:
                raise serializers.ValidationError("Bu email sistemde kayıtlıdır")
        return email


class DoctorPageSerializer(PageSerializer):
    data = DoctorSerializer(many=True)

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass


class DoctorGeneralInfoSerializer(serializers.Serializer):
    uuid = serializers.UUIDField(read_only=True)
    firstName = serializers.CharField(read_only=True)
    lastName = serializers.CharField(read_only=True)
    profileImage = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    diplomaNo = serializers.CharField()
    department = SelectSerializer(read_only=True)
    departmentId = serializers.IntegerField(write_only=True)
    profession = serializers.CharField(required=False, allow_blank=True)
    title = serializers.CharField(required=False, allow_blank=True)

    def update(self, instance, validated_data):
        try:
            instance.profileImage = validated_data.get('profileImage')
            instance.department = Department.objects.get(id=validated_data.get('departmentId'))
            instance.profession = validated_data.get('profession')
            instance.title = validated_data.get('title')
            instance.save()
            return instance
        except:
            traceback.print_exc()
            raise serializers.ValidationError("lütfen tekrar deneyiniz")

    def create(self, validated_data):
        pass


class DoctorAboutSerializer(serializers.Serializer):
    uuid = serializers.UUIDField(read_only=True)
    about = serializers.CharField(required=False, allow_blank=True)

    def update(self, instance, validated_data):
        try:
            instance.about = validated_data.get('about')
            instance.save()
            return instance
        except:
            traceback.print_exc()
            raise serializers.ValidationError("lütfen tekrar deneyiniz")

    def create(self, validated_data):
        pass


class DoctorContactInfoSerializer(serializers.Serializer):
    uuid = serializers.UUIDField(read_only=True)
    email = serializers.CharField(read_only=True)
    address = serializers.CharField(required=False, allow_blank=True)
    website = serializers.CharField(required=False, allow_blank=True)
    youtube = serializers.CharField(required=False, allow_blank=True)
    facebook = serializers.CharField(required=False, allow_blank=True)
    linkedin = serializers.CharField(required=False, allow_blank=True)
    instagram = serializers.CharField(required=False, allow_blank=True)
    mobilePhone = serializers.CharField(required=False, allow_blank=True)

    def update(self, instance, validated_data):
        try:
            user = instance.user
            user.save()
            instance.address = validated_data.get('address')
            instance.website = validated_data.get('website')
            instance.youtube = validated_data.get('youtube')
            instance.facebook = validated_data.get('facebook')
            instance.linkedin = validated_data.get('linkedin')
            instance.instagram = validated_data.get('instagram')
            instance.mobilePhone = validated_data.get('mobilePhone')
            instance.save()
            return instance
        except:
            traceback.print_exc()
            raise serializers.ValidationError("lütfen tekrar deneyiniz")

    def create(self, validated_data):
        pass


class DoctorEducationSerializer(serializers.Serializer):
    uuid = serializers.UUIDField(read_only=True)
    universityName = serializers.CharField()
    facultyName = serializers.CharField()
    departmentName = serializers.CharField()
    educationTypeId = serializers.IntegerField(write_only=True)
    educationType = SelectSerializer(read_only=True)

    def update(self, instance, validated_data):
        try:
            with transaction.atomic():
                instance.universityName = validated_data.get('universityName')
                instance.facultyName = validated_data.get('facultyName')
                instance.departmentName = validated_data.get('departmentName')
                instance.educationType = EducationType.objects.get(id=validated_data.get('educationTypeId'))
                instance.save()
                return instance
        except:
            traceback.print_exc()
            raise ValidationError("lütfen tekrar deneyiniz")

    def create(self, validated_data):
        try:
            with transaction.atomic():

                education = DoctorEducation()
                education.universityName = validated_data.get('universityName')
                education.facultyName = validated_data.get('facultyName')
                education.departmentName = validated_data.get('departmentName')
                education.educationType = EducationType.objects.get(id=validated_data.get('educationTypeId'))
                education.save()

                return education
        except:
            traceback.print_exc()
            raise ValidationError("lütfen tekrar deneyiniz")


class DoctorEducationPageSerializer(PageSerializer):
    data = DoctorEducationSerializer(many=True)

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass


class DoctorPrizeSerializer(serializers.Serializer):
    uuid = serializers.UUIDField(read_only=True)
    title = serializers.CharField(required=True)
    description = serializers.CharField(required=True)
    date = serializers.DateField(required=False, allow_null=False)
    image = serializers.CharField(required=False, allow_blank=True)

    def update(self, instance, validated_data):
        try:
            instance.title = validated_data.get('title')
            instance.description = validated_data.get('description')
            instance.date = validated_data.get('date')
            instance.image = validated_data.get('image')

            instance.save()
            return instance
        except Exception as e:
            traceback.print_exc()
            raise serializers.ValidationError("lütfen tekrar deneyiniz")

    def create(self, validated_data):
        try:
            doctor = Staff.objects.get(profile__user=self.context['request'].user)

            prize = Prize()
            prize.title = validated_data.get('title')
            prize.description = validated_data.get('description')
            prize.date = validated_data.get('date')
            prize.image = validated_data.get('image')
            prize.doctor = doctor
            prize.save()
            return prize

        except Exception as e:
            traceback.print_exc()
            raise serializers.ValidationError("lütfen tekrar deneyiniz")


class DoctorArticleSerializer(serializers.Serializer):
    uuid = serializers.UUIDField(read_only=True)
    title = serializers.CharField(required=True)
    link = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    date = serializers.DateField()

    def update(self, instance, validated_data):
        try:
            with transaction.atomic():
                instance.title = validated_data.get('title')
                instance.link = validated_data.get('link')
                instance.date = validated_data.get('date')

                instance.save()
                return instance
        except Exception as e:
            traceback.print_exc()
            raise serializers.ValidationError("lütfen tekrar deneyiniz")

    def create(self, validated_data):
        try:
            with transaction.atomic():
                doctor = Staff.objects.get(profile__user=self.context['request'].user)

                article = DoctorArticle()
                article.title = validated_data.get('title')
                article.link = validated_data.get('link')
                article.date = validated_data.get('date')
                article.doctor = doctor
                article.save()
                return article

        except Exception as e:
            traceback.print_exc()
            raise serializers.ValidationError("lütfen tekrar deneyiniz")


class DoctorArticleTimelineSerializer(serializers.Serializer):
    title = serializers.CharField()
    date = serializers.CharField()
    category = serializers.CharField()
    color = serializers.CharField(read_only=False)

    def to_representation(self, obj):
        return {

            'title': obj['title'],
            'date': obj['date'],
            'category': obj['category'],
            'color': obj['color'],

        }
