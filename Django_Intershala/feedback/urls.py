from django.urls import path
from .views import *

urlpatterns = [
    path('post_feedback/', FeedBackViewsets.as_view()),
]
