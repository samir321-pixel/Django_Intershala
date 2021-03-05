from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from user.models import User
from .models import *
from rest_framework.response import Response
from .serializers import *
from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import SearchFilter
from job_profile.models import Profile

from job_profile.serializers import ProfileSerializer


class CreateStudent(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    lookup_field = "id"


class ProfileViewSets(generics.ListAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    filter_backends = [SearchFilter, ]
    search_fields = ['profile_name', 'experience', 'employment_type', 'schedule', 'location']
