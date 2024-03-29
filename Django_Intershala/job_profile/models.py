from django.db import models
from djmoney.models.fields import MoneyField
from localflavor.in_.models import INStateField

# Create your models here.
from student.models import StudentApplication


class Skill(models.Model):
    id = models.AutoField(primary_key=True)
    skill_name = models.CharField(max_length=100, unique=True)
    user = models.ForeignKey("user.User", on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return "{} {}".format(self.skill_name, self.active)


class Profile(models.Model):
    EMPLOYMENT_TYPE = (
        ('Internship', 'Internship'),
        ('In_Office', 'In_Office'),
    )
    WORKING_SCHEDULE = (
        ('Full_Time', 'Full_time'),
        ('Part_Time', 'Part_time')
    )
    id = models.AutoField(primary_key=True)
    recruiter = models.ForeignKey("recruiter.Recruiter", on_delete=models.CASCADE, null=True)
    profile_name = models.CharField(max_length=100)
    company = models.ForeignKey("intershala_admin.IntershalaCompany", on_delete=models.CASCADE, null=True)
    experience = models.IntegerField(default=0)
    skills = models.ManyToManyField(Skill, null=True, blank=True)
    sallery = MoneyField(default=0, default_currency='INR', max_digits=11, null=True, blank=True)
    employment_type = models.CharField(max_length=50, choices=EMPLOYMENT_TYPE, default='In_Office')
    schedule = models.CharField(max_length=60, choices=WORKING_SCHEDULE, default='Full_Time')
    created_at = models.DateTimeField(auto_now=True)
    question = models.ManyToManyField("job_profile.Assessment_question", related_name='questions', null=True,
                                      blank=True)
    received_application = models.ManyToManyField("student.StudentApplication", null=True, blank=True,
                                                  related_name="received_applications")
    location = models.CharField(max_length=100)
    state = INStateField(null=True, blank=True)
    vacancy = models.IntegerField(blank=False, null=False)
    updated_at = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)
    applied_applicants = models.IntegerField(default=0)
    selected_applicants = models.IntegerField(default=0)
    rejected_applicants = models.IntegerField(default=0)
    intouch_applicants = models.IntegerField(default=0)
    total_applicants = models.IntegerField(default=0)
    immediate = models.BooleanField(default=False)

    def __str__(self):
        return "{} {}".format(self.profile_name, self.active)

    def applied_application_counter(self):
        for i in Profile.objects.filter(active=True):
            count = StudentApplication.objects.filter(profile=i, status='Applied').count()
            i.applied_applicants = count
            i.save()

    def selected_application_counter(self):
        for i in Profile.objects.filter(active=True):
            count = StudentApplication.objects.filter(profile=i, status='Selected').count()
            i.selected_applicants = count
            i.save()

    def rejected_application_counter(self):
        for i in Profile.objects.filter(active=True):
            count = StudentApplication.objects.filter(profile=i, status='Rejected').count()
            i.rejected_applicants = count
            i.save()

    def intouch_application_counter(self):
        for i in Profile.objects.filter(active=True):
            count = StudentApplication.objects.filter(profile=i, status='in_touch').count()
            i.intouch_applicants = count
            i.save()

    def total_application_counter(self):
        for i in Profile.objects.filter(active=True):
            count = StudentApplication.objects.filter(profile=i).count()
            i.total_applicants = count
            i.save()


class Assessment_question(models.Model):
    id = models.AutoField(primary_key=True)
    recruiter = models.ForeignKey("recruiter.Recruiter", on_delete=models.CASCADE)
    question = models.TextField(max_length=5000)
    profile = models.ForeignKey("job_profile.Profile", on_delete=models.CASCADE, related_name='profile_questions')
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
