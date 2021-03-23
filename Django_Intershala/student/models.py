from django.db import models
from phone_field import PhoneField
from localflavor.in_.models import INStateField
from django.core.mail import send_mail

GENDER_CHOICES = (
    ("Male", "Male"),
    ("Female", "Female"),
    ("Other", "Other"),
)


# Create your models here.
class Student(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey('user.User', on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100, unique=True)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    date_of_birth = models.DateField(auto_now=False)
    gender = models.CharField(choices=GENDER_CHOICES, max_length=30, default="Male")
    phone = PhoneField(blank=False, unique=True)
    email = models.EmailField(unique=True)
    city = models.CharField(max_length=50)
    state = INStateField(null=True, blank=True)
    applied_application = models.ManyToManyField("student.StudentApplication", null=True, blank=True,
                                                 related_name="my_application")
    active = models.BooleanField(default=True)
    password = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    get_notified = models.BooleanField(default=True)

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
    updated_at = models.DateTimeField(auto_now_add=True)
    answer = models.ManyToManyField("job_profile.Assessment_answer", blank=True, null=True)
    resume = models.URLField(max_length=800, null=False, blank=False)
    status = models.CharField(max_length=50, choices=Status, default='Applied')
    other_links = models.URLField(max_length=800, null=True, blank=True)

    def __str__(self):
        return "{} {}".format(self.student, self.status)


class StudentNotification(models.Model):
    id = models.AutoField(primary_key=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    message = models.TextField()
    seen = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{} {}".format(self.student, self.seen)

    def selected(self, student, student_name, profile_name, company_name):
        StudentNotification.objects.create(student=student,
                                           message="Congratulation {}, You are selected as {} in {}.".format(
                                               student_name,
                                               profile_name, company_name))

    def student_register(self, student, student_name, email, from_email):
        subject = "Registered Successful"
        message = "Hello {}, Welcome to Intershala Update your Intershala Profile and Get hired by Recruiters.".format(
            student_name)
        try:
            send_mail(subject, message, from_email, [email])
        except Exception as e:
            f = open('logs/student/{}.txt'.format(email), 'w+')
            f.write("Failed to send mail. {}".format(e))
            f.close()
        StudentNotification.objects.create(student=student,
                                           message="Hello {}, Welcome to Intershala Update your Intershala Profile and Get hired by Recruiters.".format(
                                               student_name))

    def notify_student(self, student, student_name, job_profile, email, from_email):
        subject = "Applied Successfully!"
        message = "Hello {}, You have successfully applied to  {}.".format(student_name, job_profile)
        try:
            send_mail(subject, message, from_email, [email])
        except Exception as e:
            f = open('logs/student/{}.txt'.format(email), 'w+')
            f.write("Failed to send mail. {}".format(e))
            f.close()
        StudentNotification.objects.create(student=student,
                                           message="Hello {}, You have successfully applied to  {}.".format(
                                               student_name, job_profile))

    def unseen_notification_counter(self):
        for i in Student.objects.all():
            count = StudentNotification.objects.filter(student=i, seen=False).count()
            i.unseen_notification = count
            i.save()

    def removed_student(self, student, student_name, email, from_email):
        subject = "Thanks to be part of intershala!"
        message = "Hello {}, Sorry to inform you but your profile has been deactivated from intershala as u have didnt follow intershala rules and regulation. please contact intershala admin support.".format(
            student_name)
        try:
            send_mail(subject, message, from_email, [email])
        except Exception as e:
            f = open('logs/student/{}.txt'.format(email), 'w+')
            f.write("Failed to send mail. {}".format(e))
            f.close()
        StudentNotification.objects.create(student=student,
                                           message="Hello {}, Sorry to inform you but your profile has been deactivated from intershala as u have didnt follow intershala rules and regulation. please contact intershala admin support.".format(
                                               student_name))

    def updated_student(self, student, student_name, email, from_email):
        subject = "Profile Updated"
        message = "Hello {}, Your profile is now activated.".format(
            student_name)
        try:
            send_mail(subject, message, from_email, [email])
        except Exception as e:
            f = open('logs/student/{}.txt'.format(email), 'w+')
            f.write("Failed to send mail. {}".format(e))
            f.close()
        StudentNotification.objects.create(student=student,
                                           message="Hello {}, Your profile is now activated.".format(
                                               student_name))
