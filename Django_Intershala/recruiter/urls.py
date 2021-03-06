from rest_framework import routers
from django.urls import path, include

from .views import *

router = routers.DefaultRouter()
router.register('manage_recruiter', CreateRecruiter, 'manage_recruiter')

urlpatterns = [
    path(r'', include(router.urls)),
    path('recruiter_notification/', RecruiterNotificationViewSets.as_view()),
]
