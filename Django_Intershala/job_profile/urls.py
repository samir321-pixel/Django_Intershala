from rest_framework import routers
from django.urls import path, include
from .views import *

router = routers.DefaultRouter()
router.register('profile', ProfileViewSet, 'profile')
urlpatterns = [
    path(r'', include(router.urls)),
    path('student_applications/<int:id>/', StudentApplicationsViewSet.as_view()),
    path('question', AssessmentQuestionViewsets.as_view()),
    path('add_question', AssessmentQuestionCreateViewsets.as_view()),
    path('student_applications/<int:id>/', StudentApplicationsViewSet.as_view()),
]
