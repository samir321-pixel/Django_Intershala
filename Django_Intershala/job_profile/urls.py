from rest_framework import routers
from django.urls import path, include
from .views import *

router = routers.DefaultRouter()
router.register('profile', ProfileViewSet, 'profile')

urlpatterns = [
    path(r'', include(router.urls)),
]
