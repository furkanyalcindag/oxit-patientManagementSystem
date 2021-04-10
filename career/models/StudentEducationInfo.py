import uuid as uuid
from django.db import models

from career.models.BaseModel import BaseModel
from career.models.Department import Department
from career.models.EducationType import EducationType
from career.models.Faculty import Faculty
from career.models.Student import Student
from career.models.University import University


class StudentEducationInfo(BaseModel):
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
