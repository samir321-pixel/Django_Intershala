from django.db import models
from djmoney.models.fields import MoneyField


# Create your models here.


class JobPosition(models.Model):
    id = models.AutoField(primary_key=True)
    job_profile = models.ForeignKey("job_profile.Profile", on_delete=models.CASCADE)
    skill = models.ManyToManyField("job_profile.Skill")
    sallery = MoneyField(default=0, default_currency='INR', max_digits=11, null=True, blank=True)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)
