from rest_framework import routers
from django.urls import path, include
from .views import *

router = routers.DefaultRouter()
router.register('profile', ProfileViewSet, 'profile')
router.register('question', AssessmentQuestionViewsets, 'question')

urlpatterns = [
    path(r'', include(router.urls)),
]
