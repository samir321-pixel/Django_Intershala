from rest_framework import routers
from django.urls import path, include

from .views import *

router = routers.DefaultRouter()
router.register('student', IntershalaStudentViewSets, 'student')

urlpatterns = [
    path(r'', include(router.urls)),
]
