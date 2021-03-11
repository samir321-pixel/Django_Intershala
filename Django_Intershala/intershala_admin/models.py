from django.db import models
from phone_field import PhoneField
from localflavor.in_.models import INStateField
from djmoney.models.fields import MoneyField

from recruiter.models import Recruiter

gender_choices = (
    ("Male", "Male"),
    ("Female", "Female"),
    ("Other", "Other"),
)

id_proof = (
    ("Aadhar Card", "Aadhar Card"),
    ("Pan Card", "Pan Card"),
)


class IntershalaCompany(models.Model):
    company_name = models.CharField(max_length=200, unique=True)
    company_description = models.TextField()
    company_established = models.DateField(auto_now=False)
    website = models.EmailField()
    rating = models.FloatField(default=0)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    recruiter = models.ManyToManyField(Recruiter)

    def __str__(self):
        return "{} {}".format(self.company_name, self.active)


class IntershalaAdmin(models.Model):
    user = models.ForeignKey("user.User", on_delete=models.CASCADE)
    first_name = models.CharField(max_length=200, null=True, blank=True)
    last_name = models.CharField(max_length=200, null=True, blank=True)
    DOB = models.DateField()
    email = models.EmailField(max_length=200, blank=True)
    gender = models.CharField(max_length=10, choices=gender_choices)
    phone = PhoneField(blank=False, unique=True)
    alt_phone = PhoneField(blank=False)
    active = models.BooleanField()
    city = models.CharField(max_length=20)
    state = INStateField(null=True, blank=True)
    pincode = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "Admin-{}".format(self.first_name)


# Create your models here.
class IntershalaEmployee(models.Model):
    user = models.ForeignKey("user.User", on_delete=models.CASCADE, null=True, blank=True)
    first_name = models.CharField(max_length=200, default="")
    middle_name = models.CharField(max_length=200, default="", )
    last_name = models.CharField(max_length=200, default="", null=True, blank=True)
    DOB = models.DateField()
    gender = models.CharField(max_length=10, choices=gender_choices)
    phone = PhoneField(blank=False, unique=True)
    alt_phone = PhoneField(blank=False)
    email = models.EmailField(unique=True)
    image = models.ImageField(upload_to="Employee/Image")
    active = models.BooleanField(default=True)
    Address = models.CharField(max_length=200)
    city = models.CharField(max_length=20)
    state = INStateField(null=True, blank=True)
    pincode = models.PositiveIntegerField(default=0)
    id_proof = models.CharField(max_length=30, choices=id_proof)
    resume = models.FileField(upload_to="Employee/Resume")
    joining_date = models.DateField()
    salary = MoneyField(default=0, default_currency='INR', max_digits=11, null=True, blank=True)
    salary_due_date = models.DateField()
    releasing_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{} {}".format(self.user, self.salary)


class EmployeeNotification(models.Model):
    employee = models.ForeignKey(IntershalaEmployee, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    seen = models.BooleanField(default=False)

    def __str__(self):
        return "{} {}".format(self.employee, self.text)


class AdminNotification(models.Model):
    text = models.TextField()
    admin = models.ForeignKey(IntershalaAdmin, on_delete=models.CASCADE, null=True)
    recruiter = models.ForeignKey("recruiter.Recruiter", on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    seen = models.BooleanField(default=False)

    def __str__(self):
        return "{}".format(self.text)

    def notify_admin(recruiter, recruiter_name):
        AdminNotification.objects.create(recruiter=recruiter,
                                         text="Hello Admin, {} want to collabrate with Intershala.".format(recruiter,
                                                                                                           recruiter_name))

    def admin_added(admin_name, admin):
        AdminNotification.objects.create(admin=admin,
                                         text="New admin, {} has been added to Intershala.".format(admin_name))

    def admin_removed(admin_name, admin):
        AdminNotification.objects.create(admin=admin,
                                         text="Admin, {} has been Removed from Intershala.".format(admin_name))
