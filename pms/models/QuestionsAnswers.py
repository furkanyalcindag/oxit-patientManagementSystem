from django.db import models

from pms.models.Answer import Answer
from pms.models.Question import Question


class QuestionsAnswers(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, null=True, blank=True)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, null=True, blank=True)
