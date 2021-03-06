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
from django.db import IntegrityError
from job_profile.serializers import ProfileSerializer


class CreateStudent(generics.CreateAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    lookup_field = "id"

    def perform_create(self, serializer):
        try:
            user = User.objects.create_user(username=self.request.data['phone'], password=self.request.data['phone'],
                                            email=self.request.data['email'],
                                            is_student=True)
        except IntegrityError:
            return Response({"USER_EXISTS": "User already exists with this phone number"}, status=400)
        serializer = self.get_serializer(data=self.request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(user=user, active=True)
            return Response(serializer.data, status=201)
        else:
            return Response(serializer.errors, status=400)


class StudentProfile(generics.RetrieveUpdateAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer


class ProfileViewSets(generics.ListAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    filter_backends = [SearchFilter, ]
    search_fields = ['profile_name', 'experience', 'employment_type', 'schedule', 'location']


class StudentApplicationViewSets(viewsets.ModelViewSet):
    queryset = StudentApplication.objects.all().order_by('-applied_on')
    serializer_class = StudentApplicationSerializer

    def list(self, request, *args, **kwargs):
        try:
            query = StudentApplication.objects.filter(student=Student.objects.get(user=self.request.user.id))
            serializer = self.get_serializer(query, many=True)
            return Response(serializer.data, status=200)
        except:
            return Response({"You are Not Student": "Access Denied"})
