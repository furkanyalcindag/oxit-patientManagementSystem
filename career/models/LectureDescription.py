from django.db import models


from career.models.BaseModel import BaseModel
from career.models.Language import Language
from career.models.Lecture import Lecture


class LectureDescription(BaseModel):
    lecture=models.ForeignKey(Lecture,on_delete=models.CASCADE)
    name=models.CharField(max_length=256,null=False)
    description=models.TextField(null=False)
    language=models.ForeignKey(Language,on_delete=models.CASCADE)





