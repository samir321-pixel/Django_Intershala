from datetime import datetime
from django.db import models
from .models import *
from django.core.mail import send_mail


class RecruiterNotification(models.Model):
    id = models.AutoField(primary_key=True)
    recruiter = models.ForeignKey(Recruiter, on_delete=models.CASCADE)
    message = models.TextField()
    seen = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{}".format(self.recruiter)

    def notify_recruiter(self, student, recruiter, recruiter_name, profile, email, from_email):
        subject = "Student Applied"
        message = "Hello {}, {} applied for {} profile. ".format(
            recruiter_name, student, profile)
        try:
            send_mail(subject, message, from_email, [email])
        except Exception as e:
            f = open('logs/recruiter/{}.txt'.format(email), 'w+')
            f.write("Failed to send mail. {}".format(e))
            f.close()
        RecruiterNotification.objects.create(recruiter=recruiter,
                                             message="Hello {}, {} applied for {} profile. ".format(recruiter_name,
                                                                                                    student, profile))

    def allow_recruiter(self, recruiter, recruiter_name, email, from_email):
        subject = "Promoted!"
        message = "Hello {}, Congratulations you are now allow to post job profile and start hiring.".format(
            recruiter_name)
        try:
            send_mail(subject, message, from_email, [email])
        except Exception as e:
            f = open('logs/recruiter/{}.txt'.format(email), 'w+')
            f.write("Failed to send mail. {}".format(e))
            f.close()
        RecruiterNotification.objects.create(recruiter=recruiter,
                                             message="Hello {}, Congratulations you are now allow to post job profile and start hiring.".format(
                                                 recruiter_name, updated_at=datetime.now()))

    def denied_recruiter(self, recruiter, recruiter_name, email, from_email):
        subject = "Thanks to be part of intershala!"
        message = "Hello {}, Sorry to let you know but you are not allow to post job profile so all the job profiles you created will be removed. please contact Intershala Admin.".format(
            recruiter_name)
        try:
            send_mail(subject, message, from_email, [email])
        except Exception as e:
            pass
        RecruiterNotification.objects.create(recruiter=recruiter,
                                             message="Hello {}, Sorry to let you know but you are not allow to post job profile so all the job profiles you created will be removed. please contact Intershala Admin.".format(
                                                 recruiter_name, updated_at=datetime.now()))

    def unseen_notification_counter(self):
        for i in Recruiter.objects.all():
            count = RecruiterNotification.objects.filter(recruiter=i, seen=False).count()
            i.unseen_notification = count
            i.save()
