from rest_framework import routers
from django.urls import path, include

from .views import *

router = routers.DefaultRouter()
router.register('manage_student', CreateStudent, 'manage_student')
router.register('student_application', StudentApplicationViewSets, 'student_application')

urlpatterns = [
    path(r'', include(router.urls)),
    path('all_profile/', ProfileViewSets.as_view()),
]
