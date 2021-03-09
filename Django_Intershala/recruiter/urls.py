from rest_framework import routers
from django.urls import path, include

from .views import *

router = routers.DefaultRouter()

urlpatterns = [
    path('recruiter_notification/', RecruiterNotificationViewSets.as_view()),
    path('recruiter_signup/', RecruiterSignin.as_view()),
    path('recruiter_profile/', RecruiterProfile.as_view()),
]
