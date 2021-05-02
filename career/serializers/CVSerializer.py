from django.db import transaction
from rest_framework import serializers

from career.models import Student, StudentEducationInfo, University, Faculty, Department


class StudentEducationInfoSerializer(serializers.Serializer):
    # TODO: Student Education Info serializer for university or master

    uuid = serializers.UUIDField(read_only=True)
    studentUUID = serializers.UUIDField(write_only=True)
    university = serializers.CharField(write_only=True, required=True)
    faculty = serializers.CharField(write_only=True, required=True)
    department = serializers.CharField(write_only=True, required=True)
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
        try:
            with transaction.atomic():
                student = Student.objects.get(uuid=validated_data.get('studentUUID'))
                university = University.objects.get(id=validated_data.get('university'))
                faculty = Faculty.objects.get(id=validated_data.get('faculty'))
                department = Department.objects.get(id=validated_data.get('department'))
                education_info = StudentEducationInfo()
                education_info.student = student

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
