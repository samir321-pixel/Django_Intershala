from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class User(AbstractUser):
    is_admin = models.BooleanField(default=False)
    is_recruiter = models.BooleanField(default=False)
    is_student = models.BooleanField(default=True)
    is_employee = models.BooleanField(default=False)
