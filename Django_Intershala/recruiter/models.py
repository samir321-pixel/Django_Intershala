from django.db import models

# Create your models here.

gender_choices = (
    ("Male", "Male"),
    ("Female", "Female"),
    ("Other", "Other"),
)


class Recruiter(models.Model):
    user = models.OneToOneField("user.User", on_delete=models.CASCADE)
    first_name = models.CharField(max_length=200, null=True)
    last_name = models.CharField(max_length=200, null=True)
    company = models.CharField(max_length=200, unique=True)
    DOB = models.DateField(null=True)
    created_profile = models.ManyToManyField("job_profile.Profile", null=True, blank=True, related_name="my_profiles")
    gender = models.CharField(max_length=10, choices=gender_choices, default="Male")
    active = models.BooleanField(default=True)
    company_address = models.CharField(max_length=200)
    city = models.CharField(max_length=20)
    state = models.CharField(max_length=200)
    pincode = models.CharField(("pin code"), max_length=7, default="00000")
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{} {}".format(self.user, self.first_name)
