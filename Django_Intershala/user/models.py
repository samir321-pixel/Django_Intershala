from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class User(AbstractUser):
    is_admin = models.BooleanField(default=False)
    is_recruiter = models.BooleanField(default=False)
    is_student = models.BooleanField(default=False)
    is_employee = models.BooleanField(default=False)
    qr_code = models.ImageField(upload_to='media/qr_codes', blank=True)
    get_notified = models.BooleanField(default=True)
