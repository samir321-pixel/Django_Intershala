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
    school_name = models.CharField(max_length=200)
    degree = models.CharField(max_length=100)
    date_added = models.DateField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{} {}".format(self.first_name, self.email)

# hey samir mujhe isme resume ke liye filed daalni hei but smjh nhi araha hei ki kese daalu vo aap krdo and tell me pleasse
