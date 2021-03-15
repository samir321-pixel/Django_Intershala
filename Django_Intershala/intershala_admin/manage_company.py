from datetime import datetime
from rest_framework import generics, viewsets
from rest_framework.permissions import IsAuthenticated
from .serializers import *
from rest_framework.response import Response
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.filters import SearchFilter

from student.models import Student


class IntershalaCompanyViewsets(viewsets.ModelViewSet):
    queryset = IntershalaCompany.objects.all()
    serializer_class = IntershalaCompanyReadSerializer
    permission_classes = [IsAuthenticated, ]
    filter_backends = [SearchFilter, ]
    search_fields = ['company_name']
    lookup_field = "id"

    def list(self, request, *args, **kwargs):
        if self.request.user.is_admin or self.request.user.is_superuser:
            query = IntershalaCompany.objects.all().order_by('-created_at')
            serializer = self.get_serializer(query, many=True)
            return Response(serializer.data, status=200)
        else:
            return Response({"NO_ACCESS": "Access Denied"}, status=401)

    def perform_create(self, serializer):
        if self.request.user.is_admin or self.request.user.is_superuser:
            serializer = IntershalaCompanyWriteSerializer(data=self.request.data)
            if serializer.is_valid(raise_exception=True):
                data = serializer.save(active=True)
                AdminNotification.company_added(company=data)
                return Response(serializer.data, status=200)
            else:
                return Response(serializer.errors, status=401)
        else:
            return Response({"NO_ACCESS": "Access Denied"}, status=401)

    def retrieve(self, request, *args, **kwargs):
        if self.request.user.is_superuser or self.request.user.is_admin:
            try:
                instance = IntershalaCompany.objects.get(id=self.kwargs["id"])
            except ObjectDoesNotExist:
                return Response({"DOES_NOT_EXIST": "Does not exist"}, status=400)
            serializer = self.get_serializer(instance)
            return Response(serializer.data, status=200)
        else:
            return Response({"NO_ACCESS": "Access Denied"}, status=401)

    def update(self, request, *args, **kwargs):
        try:
            if self.request.user.is_superuser or self.request.user.is_admin:
                try:
                    queryset = IntershalaCompany.objects.get(id=self.kwargs["id"])
                except ObjectDoesNotExist:
                    return Response({"DOES_NOT_EXIST": "Does not exist"}, status=400)
                serializer = IntershalaCompanyWriteSerializer(queryset, data=self.request.data, partial=True)
                if serializer.is_valid(raise_exception=True):
                    if serializer.validated_data.get('active'):
                        AdminNotification.company_added(company=queryset)
                        serializer.save(updated_at=datetime.now(), active=True)
                    elif not serializer.validated_data.get('active'):
                        AdminNotification.company_removed(company=queryset)
                        serializer.save(updated_at=datetime.now(), active=False)
                    return Response(serializer.data, status=200)
                else:
                    return Response(serializer.errors, status=400)
        except:
            return Response({"NO_ACCESS": "Access Denied"}, status=401)

    def destroy(self, request, *args, **kwargs):
        if self.request.user.is_superuser:
            try:
                instance = IntershalaCompany.objects.get(id=self.kwargs["id"])
            except ObjectDoesNotExist:
                return Response({"DOES_NOT_EXIST": "Does not exist"}, status=400)
            instance.active = False
            AdminNotification.company_removed(company=instance)
            instance.save()
            return Response({"Company Deleted": "Access Granted"}, status=200)
        else:
            return Response({"NO_ACCESS": "Access Denied"}, status=401)


class CompanyReviewViewsets(generics.ListCreateAPIView):
    queryset = CompanyReview.objects.all().order_by('created_at')
    serializer_class = CompanyReviewSerializer
    permission_classes = [IsAuthenticated, ]

    def create(self, request, *args, **kwargs):
        if self.request.user.is_student:
            serializer = self.get_serializer(data=self.request.data)
            if serializer.is_valid(raise_exception=True):
                student_query = Student.objects.get(user=self.request.user)
                serializer.save(student=student_query)
                IntershalaCompany.rating_counter(self=self,company_id=serializer.validated_data.get('company').id)
                return Response(serializer.data, status=200)
            else:
                return Response(serializer.errors, status=401)
        else:
            return Response({"NO_ACCESS": "Access Denied"}, status=401)

    def list(self, request, *args, **kwargs):
        if self.request.user.is_student:
            queryset = CompanyReview.objects.filter(student=Student.objects.get(user=self.request.user)).order_by(
                'created_at')
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data, status=200)
        else:
            return Response({"NO_ACCESS": "Access Denied"}, status=401)
