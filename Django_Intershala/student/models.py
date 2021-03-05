from django.db import models
from phone_field import PhoneField
from localflavor.in_.models import INStateField

GENDER_CHOICES = (
    ("Male", "Male"),
    ("Female", "Female"),
    ("Other", "Other"),
)


# Create your models here.
class Student(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey('user.User', on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    date_of_birth = models.DateField(auto_now=False)
    gender = models.CharField(choices=GENDER_CHOICES, max_length=30, default="Male")
    phone = PhoneField(blank=False)
    email = models.EmailField()
    city = models.CharField(max_length=50)
    state = INStateField(null=True, blank=True)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{} {}".format(self.first_name, self.email)


class StudentApplication(models.Model):
    Status = (
        ('Selected', 'Selected'),
        ('Rejected', 'Rejected'),
        ('in_touch', 'in_touch'),
        ('Applied', 'Applied'),
    )
    id = models.AutoField(primary_key=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    profile = models.ForeignKey("job_profile.Profile", on_delete=models.CASCADE)
    active = models.BooleanField(default=True)
    applied_on = models.DateTimeField(auto_now=True)
    answer = models.ManyToManyField("job_profile.Assessment_answer", blank=True, null=True)
    resume = models.URLField(max_length=800, null=False, blank=False)
    status = models.CharField(max_length=50, choices=Status, default='Applied')
    other_links = models.URLField(max_length=800, null=True, blank=True)

    def __str__(self):
        return "{} {}".format(self.student, self.status)
