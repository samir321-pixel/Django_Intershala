from django.db import models

# Create your models here.

gender_choices = (
    ("Male", "Male"),
    ("Female", "Female"),
    ("Other", "Other"),
)


class Recruiter(models.Model):
    user = models.OneToOneField("user.User", on_delete=models.PROTECT)
    first_Name = models.CharField(max_length=200)
    middle_Name = models.CharField(max_length=200)
    company = models.CharField(max_length=200, unique=True)
    last_Name = models.CharField(max_length=200, default="", null=True, blank=True)
    DOB = models.DateField()
    gender = models.CharField(max_length=10, choices=gender_choices)
    active = models.BooleanField(default=True)
    Address = models.CharField(max_length=200, null=True, blank=True)
    city = models.CharField(max_length=20, null=True, blank=True)
    state = models.CharField(max_length=200, null=True, blank=True)
    pincode = models.CharField(("pin code"), max_length=7, default="00000")
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{} {}".format(self.user, self.first_Name)
