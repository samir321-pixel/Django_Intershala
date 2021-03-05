from datetime import datetime

from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated
from .serializers import *
# Create your views here.
from student.models import Student
from recruiter.models import Recruiter
from job_profile.models import Profile, Skill
from rest_framework.response import Response
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.filters import SearchFilter


class IntershalaStudentViewSets(generics.ListAPIView, generics.DestroyAPIView):
    queryset = Student.objects.all().order_by('-created_at')
    serializer_class = IntershalaStudentSerializer
    permission_classes = (IsAuthenticated,)
    lookup_field = "id"
    filter_backends = [SearchFilter, ]
    search_fields = ['first_name', 'email']

    def list(self, request, *args, **kwargs):
        if self.request.user.is_employee or self.request.user.is_superuser or self.request.user.is_admin:
            queryset = self.get_queryset()
            queryset = self.filter_queryset(queryset)
            queryset = self.filter_queryset(queryset)
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data, status=200)
        else:
            return Response({"NO_ACCESS": "Access Denied"}, status=401)

    def destroy(self, request, *args, **kwargs):
        if self.request.user.is_employee or self.request.user.is_superuser or self.request.user.is_admin:
            try:
                instance = self.queryset.get(id=self.kwargs["id"])
            except ObjectDoesNotExist:
                return Response({"DOES_NOT_EXIST": "Does not exist"}, status=400)
            instance.delete()
            return Response({"Student Deleted": "Access Granted"}, status=200)
        else:
            return Response({"NO_ACCESS": "Access Denied"}, status=401)


class IntershalaRecruiterViewSets(generics.ListAPIView, generics.DestroyAPIView):
    queryset = Profile.objects.all().order_by('-created_at')
    serializer_class = IntershalaRecruiterSerializer
    permission_classes = (IsAuthenticated,)
    lookup_field = "id"
    filter_backends = [SearchFilter, ]
    search_fields = ['first_name', 'email', 'company', 'active']

    def list(self, request, *args, **kwargs):
        if self.request.user.is_employee or self.request.user.is_superuser or self.request.user.is_admin:
            queryset = self.get_queryset()
            queryset = self.filter_queryset(queryset)
            queryset = self.filter_queryset(queryset)
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data, status=200)
        else:
            return Response({"NO_ACCESS": "Access Denied"}, status=401)

    def destroy(self, request, *args, **kwargs):
        if self.request.user.is_employee or self.request.user.is_superuser or self.request.user.is_admin:
            try:
                instance = self.queryset.get(id=self.kwargs["id"])
            except ObjectDoesNotExist:
                return Response({"DOES_NOT_EXIST": "Does not exist"}, status=400)
            instance.delete()
            return Response({"Recruiter Deleted": "Access Granted"}, status=200)
        else:
            return Response({"NO_ACCESS": "Access Denied"}, status=401)


class IntershalaJobProfileViewSets(generics.ListAPIView, generics.DestroyAPIView, generics.RetrieveUpdateAPIView):
    queryset = Profile.objects.all().order_by('-created_at')
    serializer_class = IntershalaJobProfileReadSerializer
    permission_classes = (IsAuthenticated,)
    lookup_field = "id"
    filter_backends = [SearchFilter, ]
    search_fields = ['profile_name', 'skills__skill_name', 'active']

    def list(self, request, *args, **kwargs):
        if self.request.user.is_employee or self.request.user.is_superuser or self.request.user.is_admin:
            queryset = self.get_queryset()
            queryset = self.filter_queryset(queryset)
            queryset = self.filter_queryset(queryset)
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data, status=200)
        else:
            return Response({"NO_ACCESS": "Access Denied"}, status=401)

    def retrieve(self, request, *args, **kwargs):
        if self.request.user.is_admin or self.request.user.is_employee or self.request.user.is_customer:
            try:
                queryset = Profile.objects.get(id=self.kwargs["id"])
                serializer = IntershalaJobProfileReadSerializer(queryset)
                return Response(serializer.data, status=200)
            except:
                return Response({"DOES_NOT_EXIST": "Does not exist"}, status=400)
        else:
            return Response({"NO_ACCESS": "Access Denied"}, status=401)

    def update(self, request, *args, **kwargs):
        try:
            if self.request.user.is_admin or self.request.user.is_employee:
                try:
                    queryset = Profile.objects.get(id=self.kwargs["id"])
                    serializer = self.get_serializer(queryset, data=self.request.data, partial=True)
                    if serializer.is_valid(raise_exception=True):
                        serializer.save(updated_at=datetime.now())
                        return Response(serializer.data, status=200)
                    else:
                        return Response(serializer.errors, status=400)
                except ObjectDoesNotExist:
                    return Response({"DOES_NOT_EXIST": "Does not exist"}, status=400)
        except:
            return Response({"NO_ACCESS": "Access Denied"}, status=401)

    def destroy(self, request, *args, **kwargs):
        if self.request.user.is_employee or self.request.user.is_superuser or self.request.user.is_admin:
            try:
                instance = self.queryset.get(id=self.kwargs["id"])
            except ObjectDoesNotExist:
                return Response({"DOES_NOT_EXIST": "Does not exist"}, status=400)
            instance.delete()
            return Response({"Recruiter Deleted": "Access Granted"}, status=200)
        else:
            return Response({"NO_ACCESS": "Access Denied"}, status=401)


class IntershalaSkillViewSets(generics.ListCreateAPIView):
    queryset = Skill.objects.all().order_by('-created_at')
    serializer_class = IntershalaSkillReadSerializer
    permission_classes = (IsAuthenticated,)
    filter_backends = [SearchFilter, ]
    search_fields = ['skill_name', 'active']

    def list(self, request, *args, **kwargs):
        if self.request.user.is_employee or self.request.user.is_superuser or self.request.user.is_admin:
            queryset = self.get_queryset()
            queryset = self.filter_queryset(queryset)
            queryset = self.filter_queryset(queryset)
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data, status=200)
        else:
            return Response({"NO_ACCESS": "Access Denied"}, status=401)

    def create(self, request, *args, **kwargs):
        if self.request.user.is_employee or self.request.user.is_superuser or self.request.user.is_admin:
            serializer = IntershalaSkillReadSerializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save(active=True)
                return Response(serializer.data, status=200)
            else:
                return Response(serializer.errors, status=400)
        else:
            return Response({"NO_ACCESS": "Access Denied"}, status=401)


class IntershalaSkillUpdateViewSets(generics.RetrieveUpdateDestroyAPIView):
    queryset = Skill.objects.all().order_by('-created_at')
    serializer_class = IntershalaSkillReadSerializer
    permission_classes = (IsAuthenticated,)
    lookup_field = "id"

    def retrieve(self, request, *args, **kwargs):
        if self.request.user.is_admin or self.request.user.is_employee or self.request.user.is_superuser:
            try:
                queryset = Skill.objects.get(id=self.kwargs["id"])
                serializer = self.get_serializer(queryset)
                return Response(serializer.data, status=200)
            except:
                return Response({"DOES_NOT_EXIST": "Does not exist"}, status=400)
        else:
            return Response({"NO_ACCESS": "Access Denied"}, status=401)

    def update(self, request, *args, **kwargs):
        try:
            if self.request.user.is_admin or self.request.user.is_employee or self.request.user.is_superuser:
                try:
                    queryset = Skill.objects.get(id=self.kwargs["id"])
                    serializer = self.get_serializer(queryset, data=self.request.data, partial=True)
                    if serializer.is_valid(raise_exception=True):
                        print(queryset, request.data)
                        serializer.save(updated_at=datetime.now())
                        return Response(serializer.data, status=200)
                    else:
                        return Response(serializer.errors, status=400)
                except ObjectDoesNotExist:
                    return Response({"DOES_NOT_EXIST": "Does not exist"}, status=400)
        except:
            return Response({"NO_ACCESS": "Access Denied"}, status=401)

    def destroy(self, request, *args, **kwargs):
        if self.request.user.is_employee or self.request.user.is_superuser or self.request.user.is_admin:
            try:
                instance = self.queryset.get(id=self.kwargs["id"])
            except ObjectDoesNotExist:
                return Response({"DOES_NOT_EXIST": "Does not exist"}, status=400)
            instance.delete()
            return Response({"Skill Deleted": "Access Granted"}, status=200)
        else:
            return Response({"NO_ACCESS": "Access Denied"}, status=401)
