from django.db import models
from .models import *
from job_profile.models import Profile

from student.models import Student


class RecruiterNotification(models.Model):
    id = models.AutoField(primary_key=True)
    recruiter = models.ForeignKey(Recruiter, on_delete=models.CASCADE)
    message = models.TextField()
    seen = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{} {}".format(self.recruiter, self.seen)

    def notify_recruiter(self, student, recruiter, recruiter_name, profile):
        RecruiterNotification.objects.create(recruiter=recruiter,
                                             message="Hello {}, {} applied for {} profile. ".format(recruiter_name,
                                                                                                 student, profile))

    def unseen_notification_counter(self):
        for i in Recruiter.objects.all():
            count = RecruiterNotification.objects.filter(recruiter=i, seen=False).count()
            i.unseen_notification = count
            i.save()
