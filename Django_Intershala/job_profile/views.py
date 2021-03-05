from rest_framework import viewsets
from .models import *
from .serializers import *
from rest_framework.response import Response
from django.core.exceptions import ObjectDoesNotExist
import datetime

from recruiter.models import Recruiter


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    lookup_field = "id"

    def list(self, request, *args, **kwargs):
        if self.request.user.is_recruiter:
            query = Profile.objects.filter(recruiter=Recruiter.objects.get(user=self.request.user.id)).order_by(
                '-created_at')
            serializer = self.get_serializer(query, many=True)
            return Response(serializer.data)
        else:
            return Response({"NO_ACCESS": "Access Denied"}, status=401)

    def perform_create(self, serializer):
        try:
            if self.request.user.is_recruiter:
                serializer = self.get_serializer(data=self.request.data)
                if serializer.is_valid(raise_exception=True):
                    serializer.save(recruiter=Recruiter.objects.get(user=self.request.user.id), active=True)
                    return Response(serializer.data, status=200)
                else:
                    return Response(serializer.errors, status=401)
        except:
            return Response({"NO_ACCESS": "Access Denied"}, status=401)

    def update(self, request, *args, **kwargs):
        if self.request.user.is_recruiter:
            try:
                instance = Profile.objects.get(id=self.kwargs["id"],
                                               recruiter=Recruiter.objects.get(user=self.request.user.id))
            except ObjectDoesNotExist:
                return Response({"DOES_NOT_EXIST": "Does not exist"}, status=400)
            serializer = self.get_serializer(instance, data=self.request.data, partial=True)
            if serializer.is_valid(raise_exception=True):
                serializer.save(updated_at=datetime.datetime.now())
                return Response(serializer.data)
            else:
                return Response(serializer.errors, status=401)
        else:
            return Response({"NO_ACCESS": "Access Denied"}, status=401)

    def destroy(self, request, *args, **kwargs):
        if self.request.user.is_recruiter:
            try:
                instance = Profile.objects.get(id=self.kwargs["id"],
                                               recruiter=Recruiter.objects.get(user=self.request.user.id))
            except ObjectDoesNotExist:
                return Response({"DOES_NOT_EXIST": "Does not exist"}, status=400)
            instance.delete()
            return Response({"Profile Deleted": "Access Granted"}, status=200)
        else:
            return Response({"NO_ACCESS": "Access Denied"}, status=401)

    def retrieve(self, request, *args, **kwargs):
        if self.request.user.is_recruiter:
            try:
                instance = Profile.objects.get(id=self.kwargs["id"],
                                               recruiter=Recruiter.objects.get(user=self.request.user.id))
                serializer = self.get_serializer(instance)
                return Response(serializer.data)
            except ObjectDoesNotExist:
                return Response({"DOES_NOT_EXIST": "Does not exist"}, status=400)
        else:
            return Response({"NO_ACCESS": "Access Denied"}, status=401)
