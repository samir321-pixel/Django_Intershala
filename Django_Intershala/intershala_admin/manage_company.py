from datetime import datetime
from rest_framework import generics, viewsets
from rest_framework.permissions import IsAuthenticated
from .serializers import *
from recruiter.models import Recruiter
from rest_framework.response import Response
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.filters import SearchFilter
from user.models import User
from recruiter.notification_models import RecruiterNotification


class IntershalaCompanyViewsets(viewsets.ModelViewSet):
    queryset = IntershalaCompany.objects.all()
    serializer_class = IntershalaCompanySerializer
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
            serializer = self.get_serializer(data=self.request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
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
                serializer = self.get_serializer(queryset, data=self.request.data, partial=True)
                if serializer.is_valid(raise_exception=True):
                    serializer.save(updated_at=datetime.now())
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
            instance.save()
            return Response({"Company Deleted": "Access Granted"}, status=200)
        else:
            return Response({"NO_ACCESS": "Access Denied"}, status=401)
