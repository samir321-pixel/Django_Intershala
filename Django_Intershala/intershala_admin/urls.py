from rest_framework import routers
from django.urls import path, include

from .views import *
from .manage_recruiter import *

router = routers.DefaultRouter()
router.register('intershala_employee', IntershalaEmployeeViewSets, 'intershala_employee ')
urlpatterns = [
    path(r'', include(router.urls)),
    path('manage_student/', IntershalaStudentViewSets.as_view()),
    path('manage_recruiter/', IntershalaRecruiterListView.as_view()),
    path('manage_recruiter/<int:id>/', IntershalaRecruiterUpdateView.as_view()),
    path('manage_profile/', IntershalaJobProfileViewSets.as_view()),
    path('manage_skill/', IntershalaSkillViewSets.as_view()),
    path('manage_skill/<int:id>/', IntershalaSkillUpdateViewSets.as_view()),
]
