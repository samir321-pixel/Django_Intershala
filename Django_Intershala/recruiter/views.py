from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from user.models import User
from .models import *
from rest_framework.response import Response
from .serializers import *
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated


# Create your views here.
class CreateRecruiter(viewsets.ModelViewSet):
    queryset = Recruiter.objects.all()
    serializer_class = RecruiterSerializer
    permission_classes = (IsAuthenticated,)
    lookup_field = "id"

    def create(self, request, *args, **kwargs):
        if request.user.is_admin or self.request.user.is_superuser:
            serializer = self.get_serializer(data=request.data)
            user_query = User.objects.get(id=request.data.get('user'))
            user_query.is_recruiter = True
            user_query.save()
            if serializer.is_valid(raise_exception=True):
                serializer.save(first_Name=user_query.first_name, last_Name=user_query.last_name)
            return Response(serializer.data, status=200)
        else:
            return Response({"NO_ACCESS": "Access Denied"}, status=401)

    def retrieve(self, request, *args, **kwargs):
        if request.user.is_admin or self.request.user.is_superuser:
            try:
                queryset = Recruiter.objects.get(id=self.kwargs["id"])
                serializer = RecruiterSerializer(queryset)
                return Response(serializer.data, status=200)
            except ObjectDoesNotExist:
                return Response({"DOES_NOT_EXIST": "Does not exist"}, status=400)
        else:
            return Response({"NO_ACCESS": "Access Denied"}, status=401)

    def perform_update(self, serializer):
        try:
            if self.request.user.is_admin or self.request.user.is_superuser:
                try:
                    queryset = Recruiter.objects.get(id=self.kwargs["id"])
                    serializer = RecruiterSerializer(queryset, data=self.request.data, partial=True)
                    if serializer.is_valid(raise_exception=True):
                        serializer.save()
                        return Response(serializer.data, status=200)
                except ObjectDoesNotExist:
                    return Response({"DOES_NOT_EXIST": "Does not exist"}, status=400)
        except:
            return Response({"NO_ACCESS": "Access Denied"}, status=401)

    def perform_destroy(self, instance):
        try:
            if self.request.user.is_admin or self.request.user.is_superuser:
                try:
                    queryset = Recruiter.objects.get(id=self.kwargs["id"])
                    user_query = User.objects.get(id=queryset.user.id)
                    user_query.is_recruiter = False
                    user_query.save()
                    queryset.delete()
                    return Response({"Successful": "successful"}, status=204)
                except ObjectDoesNotExist:
                    return Response({"DOES_NOT_EXIST": "Does not exist"}, status=400)
            else:
                return Response({"NO_ACCESS": "Access Denied"}, status=401)
        except:
            return Response({"NO_ACCESS": "Access Denied"}, status=401)

