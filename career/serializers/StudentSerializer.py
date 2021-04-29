import traceback

from django.contrib.auth.models import User, Group
from django.db import transaction
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from career.models import Profile, Student
from career.serializers.GeneralSerializers import PageSerializer

from oxiterp.serializers import UserSerializer


class StudentSerializer(serializers.Serializer):
    # TODO: Student serializer
    uuid = serializers.UUIDField(read_only=True)
    user = UserSerializer(read_only=True)
    firstName = serializers.CharField(required=False)
    lastName = serializers.CharField(required=False)
    username = serializers.CharField(write_only=True, required=False,
                                     validators=[UniqueValidator(queryset=User.objects.all())])
    password = serializers.CharField(write_only=True)
    studentNumber = serializers.CharField(required=True)

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        try:
            with transaction.atomic():
                user = User.objects.create_user(username=validated_data.get('username'),
                                                email=validated_data.get('username'))
                user.first_name = validated_data.get("firstName")
                user.last_name = validated_data.get("lastName")
                user.set_password(validated_data.get('password'))
                user.save()

                group = Group.objects.get(name='Student')
                user.groups.add(group)
                user.save()
                profile = Profile.objects.create(user=user)
                profile.save()
                student = Student(profile=profile)
                student.studentNumber = validated_data.get("studentNumber")
                student.isGraduated = False
                student.save()
                return student

        except Exception as e:
            traceback.print_exc()
            raise serializers.ValidationError("lütfen tekrar deneyiniz")


class StudentPageableSerializer(PageSerializer):
    data = StudentSerializer(many=True)

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass


class StudentEducationInfoSerializer(serializers.Serializer):
    # TODO: Student Education Info serializer for university or master
    '''
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    university = models.ForeignKey(University, on_delete=models.CASCADE, null=True)
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE, null=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, null=True)
    otherUniversityName = models.CharField(max_length=256)
    otherFacultyName = models.CharField(max_length=256)
    otherDepartmentName = models.CharField(max_length=256)
    isGraduated = models.BooleanField(default=False)
    startDate = models.DateField()
    graduationDate = models.DateField()
    highSchool = models.CharField(max_length=256)
    educationType = models.ForeignKey(EducationType, on_delete=models.CASCADE)
    gpa = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    isQuaternarySystem = models.BooleanField(default=True)
    '''

    uuid = serializers.UUIDField(read_only=True)
    studentUUID = serializers.UUIDField(write_only=True)
    university = serializers.CharField(write_only=True, required=True)
    faculty = serializers.CharField(write_only=True, required=True)
    department = serializers.CharField(write_only=True,required=True)
    isGraduated = serializers.BooleanField(required=True)
    startDate = serializers.DateField(required=True)
    graduationDate = serializers.DateField(required=False)
    educationType = serializers.CharField(write_only=True)
    isQuaternarySystem = serializers.BooleanField()
    gpa = serializers.DecimalField(max_digits=10, decimal_places=2)


    def validate(self, data):
        # here you can access all values
        department = data['department']

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass

