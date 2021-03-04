from rest_framework import routers
from django.urls import path, include

from .views import *

router = routers.DefaultRouter()
router.register('manage_student', CreateStudent, 'manage_student')

urlpatterns = [
    path(r'', include(router.urls)),
]

























