from django.db import models


# Create your models here.
class Skill(models.Model):
    id = models.AutoField(primary_key=True)
    skill_name = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return "{} {}".format(self.skill_name, self.active)


class Profile(models.Model):
    id = models.AutoField(primary_key=True)
    recruiter = models.ForeignKey("recruiter.Recruiter", on_delete=models.CASCADE)
    profile_name = models.CharField(max_length=100)
    skills = models.ManyToManyField(Skill, null=True, blank=True)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return "{} {}".format(self.profile_name, self.active)


class Assessment_question(models.Model):
    id = models.AutoField(primary_key=True)
    profile = models.ForeignKey("job_profile.Profile", on_delete=models.CASCADE, related_name='profile_questions')
    recruiter = models.ForeignKey("recruiter.Recruiter", on_delete=models.CASCADE)
    question = models.TextField(max_length=5000)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.question


class Assessment_answer(models.Model):
    application_id = models.ForeignKey("job_profile.Profile", on_delete=models.CASCADE)
    student = models.ForeignKey("student.Student", on_delete=models.CASCADE)
    question = models.ForeignKey(Assessment_question, on_delete=models.CASCADE)
    answer = models.TextField(max_length=1000)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{} {}".format(self.question, self.answer)
