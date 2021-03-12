from django.contrib import admin
from .models import *
from .notification_models import *


# Register your models here.

class RecruiterReviewAdmin(admin.ModelAdmin):
    list_display = ['student', 'recruiter', 'rating']

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


admin.site.register(Recruiter)
admin.site.register(RecruiterNotification)
admin.site.register(RecruiterReview, RecruiterReviewAdmin)
