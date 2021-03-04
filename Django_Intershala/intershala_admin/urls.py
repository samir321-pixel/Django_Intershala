from rest_framework import routers
from django.urls import path

from .views import *

urlpatterns = [
    path('student/', IntershalaStudentViewSets.as_view()),
    path('recruiter/', IntershalaRecruiterViewSets.as_view()),
    path('profile/', IntershalaJobProfileViewSets.as_view()),
]
