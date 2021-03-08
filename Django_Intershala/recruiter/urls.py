from rest_framework import routers
from django.urls import path, include

from .views import *

router = routers.DefaultRouter()
#router.register('manage_recruiter', CreateRecruiter, 'manage_recruiter')

urlpatterns = [
    path('recruiter_notification/', RecruiterNotificationViewSets.as_view()),
    path('recruiter_signup/', RecruiterSignin.as_view()),
]
