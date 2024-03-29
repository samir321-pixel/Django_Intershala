from rest_framework import routers
from django.urls import path, include

from .manage_company import *
from .views import *
from .manage_recruiter import *
from .admin_notification import *

router = routers.DefaultRouter()
router.register('intershala_employee', IntershalaEmployeeViewSets, 'intershala_employee ')
router.register('manage_company', IntershalaCompanyViewsets, 'manage_company ')
urlpatterns = [
    path(r'', include(router.urls)),
    path('manage_student/', IntershalaStudentViewSets.as_view()),
    path('manage_student/<int:id>/', IntershalaStudentUpdateViewSets.as_view()),
    path('manage_recruiter/', IntershalaRecruiterListView.as_view()),
    path('manage_recruiter/<int:id>/', IntershalaRecruiterUpdateView.as_view()),
    path('manage_admin/', IntershalaAdminListView.as_view()),
    path('manage_admin/<int:id>/', IntershalaAdminUpdateView.as_view()),
    path('admin_notification/', AdminNotificationViewsets.as_view()),
    path('admin_notification/<int:id>', AdminNotificationRetriveViewsets.as_view()),
    path('employee_notification/', EmployeeNotificationViewsets.as_view()),
    path('employee_notification/<int:id>', EmployeeNotificationRetriveViewsets.as_view()),
    path('manage_profile/', IntershalaJobProfileViewSets.as_view()),
    path('manage_skill/', IntershalaSkillViewSets.as_view()),
    path('manage_skill/<int:id>/', IntershalaSkillUpdateViewSets.as_view()),
    path('company_review/', CompanyReviewViewsets.as_view()),
]
