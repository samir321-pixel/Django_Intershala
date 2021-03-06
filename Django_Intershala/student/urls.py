from rest_framework import routers
from django.urls import path, include

from .views import *

router = routers.DefaultRouter()


urlpatterns = [
    path(r'', include(router.urls)),
    path('all_job_profile/', ProfileViewSets.as_view()),
    path('student_signup/', CreateStudent.as_view()),
    path('student_profile/', StudentProfile.as_view()),
    path('student_application/', StudentApplicationViewSets.as_view()),
]
