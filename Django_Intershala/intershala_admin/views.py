from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated
from .serializers import *
# Create your views here.
from student.models import Student
from recruiter.models import Recruiter
from rest_framework.response import Response
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.filters import SearchFilter


class IntershalaStudentViewSets(generics.ListAPIView, generics.DestroyAPIView):
    queryset = Student.objects.all().order_by('-created_at')
    serializer_class = IntershalaStudentSerializer
    permission_classes = (IsAuthenticated,)
    lookup_field = "id"
    filter_backends = [SearchFilter, ]
    search_fields = ['first_name', 'email', 'date']

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
    queryset = Recruiter.objects.all().order_by('-created_at')
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
