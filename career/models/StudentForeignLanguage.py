import uuid as uuid
from django.db import models

from career.models.BaseModel import BaseModel
from career.models.ForeignLanguage import ForeignLanguage
from career.models.ForeignLanguageLevel import ForeignLanguageLevel
from career.models.Student import Student


class StudentForeignLanguage(BaseModel):
    foreignLanguage = models.ForeignKey(ForeignLanguage, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    readingLevel = models.ForeignKey(ForeignLanguageLevel, on_delete=models.CASCADE)
    writingLevel = models.ForeignKey(ForeignLanguageLevel, on_delete=models.CASCADE)
    listeningLevel = models.ForeignKey(ForeignLanguageLevel, on_delete=models.CASCADE)
    speakingLevel = models.ForeignKey(ForeignLanguageLevel, on_delete=models.CASCADE)