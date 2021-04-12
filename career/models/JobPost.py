from django.db import models

from career.models.BaseModel import BaseModel
from career.models.City import City
from career.models.Company import Company
from career.models.District import District
from career.models.JobType import JobType
from career.models.MilitaryStatus import MilitarySituation


class JobPost(BaseModel):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    title = models.CharField(max_length=256)
    quality = models.TextField()
    jobDescription = models.TextField()
    type = models.ForeignKey(JobType, on_delete=models.CASCADE)
    salaryMin = models.IntegerField()
    salaryMax = models.IntegerField()
    staffCount = models.IntegerField()
    experienceYear = models.IntegerField()
    militarySituation = models.ForeignKey(MilitarySituation, on_delete=models.CASCADE)
    startDate = models.DateField()
    finishDate = models.DateField()
    viewCount = models.IntegerField()
    city = models.ForeignKey(City ,on_delete=models.CASCADE)
    district = models.ForeignKey(District, on_delete=models.CASCADE)

