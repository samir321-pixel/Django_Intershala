from django.db import models


# Create your models here.
class Skill(models.Model):
    id = models.AutoField(primary_key=True)
    skill_name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return "{} {}".format(self.skill_name, self.active)


class Profile(models.Model):
    id = models.AutoField(primary_key=True)
    profile_name = models.CharField(max_length=100)
    skills = models.ManyToManyField(Skill)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return "{} {}".format(self.profile_name, self.active)
