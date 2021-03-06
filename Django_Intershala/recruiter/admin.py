from django.contrib import admin
from .models import *
from .notification_models import *
# Register your models here.
admin.site.register(Recruiter)
admin.site.register(RecruiterNotification)