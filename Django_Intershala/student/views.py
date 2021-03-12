from datetime import datetime
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
from recruiter.notification_models import RecruiterNotification

from recruiter.models import Recruiter


class CreateStudent(generics.CreateAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    lookup_field = "id"

    def perform_create(self, serializer):
        try:
            user = User.objects.create_user(username=self.request.data['first_name'],
                                            last_name=self.request.data['last_name'],
                                            first_name=self.request.data['first_name'],
                                            password=self.request.data['phone'],
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

    def retrieve(self, request, *args, **kwargs):
        if self.request.user.is_student:
            try:
                instance = Student.objects.get(user=self.request.user.id)
            except ObjectDoesNotExist:
                return Response({"DOES_NOT_EXIST": "Does not exist"}, status=400)
            serializer = self.get_serializer(instance)
            return Response(serializer.data, status=200)
        else:
            return Response({"NO_ACCESS": "Access Denied"}, status=401)

    def update(self, request, *args, **kwargs):
        if self.request.user.is_student:
            try:
                instance = Student.objects.get(user=self.request.user.id)
            except ObjectDoesNotExist:
                return Response({"DOES_NOT_EXIST": "Does not exist"}, status=400)
            serializer = self.get_serializer(instance, data=self.request.data, partial=True)
            if serializer.is_valid(raise_exception=True):
                serializer.save(updated_at=datetime.now())
                return Response(serializer.data)
            else:
                return Response(serializer.errors, status=401)
        else:
            return Response({"NO_ACCESS": "Access Denied"}, status=401)


class ProfileViewSets(generics.ListAPIView):
    queryset = Profile.objects.all()
    serializer_class = JobProfileReadSerializer
    filter_backends = [SearchFilter, ]
    search_fields = ['profile_name', 'experience', 'employment_type', 'schedule', 'location', 'recruiter__company']


class StudentApplicationViewSets(generics.ListCreateAPIView):
    queryset = StudentApplication.objects.all().order_by('-applied_on')
    serializer_class = StudentApplicationSerializer

    def list(self, request, *args, **kwargs):
        try:
            query = StudentApplication.objects.filter(student=Student.objects.get(user=self.request.user.id))
            serializer = self.get_serializer(query, many=True)
            return Response(serializer.data, status=200)
        except:
            return Response({"You are Not Student": "Access Denied"})

    def create(self, request, *args, **kwargs):
        if self.request.user.is_student:
            serializer = self.get_serializer(data=self.request.data)
            if serializer.is_valid(raise_exception=True):
                data = serializer.save(student=Student.objects.get(user=self.request.user.id), status='Applied',
                                       active=True)
                student_query = Student.objects.get(user=self.request.user.id)
                profile_query = Profile.objects.get(id=self.request.data.get('profile'))
                recruiter_query = Recruiter.objects.get(id=profile_query.recruiter.id)
                profile_query.received_application.add(data)
                student_query.applied_application.add(data)
                RecruiterNotification.notify_recruiter(self=self, student=student_query.first_name,
                                                       recruiter=recruiter_query,
                                                       recruiter_name=recruiter_query.first_name,
                                                       profile=profile_query)
                StudentNotification.notify_student(self=self, student=student_query,
                                                   student_name=student_query.first_name, job_profile=profile_query)
                RecruiterNotification.unseen_notification_counter(self=self)
                StudentNotification.unseen_notification_counter(self=self)
                return Response(serializer.data, status=200)
            else:
                return Response(serializer.errors, status=400)
        else:
            return Response({"NO_ACCESS": "Access Denied"}, status=401)


class StudentNotificationViewSets(generics.ListAPIView):
    queryset = StudentNotification.objects.all().order_by('-created_at')
    serializer_class = StudentNotificationSerializer
    permission_classes = [IsAuthenticated, ]

    def list(self, request, *args, **kwargs):
        if self.request.user.is_student:
            queryset = StudentNotification.objects.filter(
                student=Student.objects.get(user=self.request.user.id)).order_by('-created_at')
            queryset.update(seen=True)
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data, status=200)
        else:
            return Response({"NO_ACCESS": "Access Denied"}, status=401)
