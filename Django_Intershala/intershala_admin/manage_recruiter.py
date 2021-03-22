`from datetime import datetime
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .serializers import *
from recruiter.models import Recruiter
from rest_framework.response import Response
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.filters import SearchFilter
from user.models import User
from recruiter.notification_models import RecruiterNotification

from job_profile.models import Profile

from Django_Intershala.settings import EMAIL_HOST_USER


class IntershalaRecruiterListView(generics.ListAPIView):
    queryset = Recruiter.objects.all().order_by('-created_at')
    serializer_class = IntershalaRecruiterSerializer
    permission_classes = (IsAuthenticated,)
    lookup_field = "id"
    filter_backends = [SearchFilter, ]
    search_fields = ['first_name', 'company', 'active']

    def list(self, request, *args, **kwargs):
        if self.request.user.is_employee or self.request.user.is_superuser or self.request.user.is_admin:
            queryset = self.get_queryset()
            queryset = self.filter_queryset(queryset)
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data, status=200)
        else:
            return Response({"NO_ACCESS": "Access Denied"}, status=401)


class IntershalaRecruiterUpdateView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Recruiter.objects.all().order_by('-created_at')
    serializer_class = IntershalaRecruiterSerializer
    permission_classes = (IsAuthenticated,)
    lookup_field = "id"

    def retrieve(self, request, *args, **kwargs):
        if request.user.is_admin or request.user.is_employee or self.request.user.is_superuser:
            try:
                queryset = Recruiter.objects.get(id=self.kwargs["id"])
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
                    queryset = Recruiter.objects.get(id=self.kwargs["id"])
                    serializer = self.get_serializer(queryset, data=self.request.data, partial=True)
                    if serializer.is_valid(raise_exception=True):
                        if serializer.validated_data.get('active'):
                            RecruiterNotification.allow_recruiter(self=self, recruiter=queryset,
                                                                  recruiter_name=queryset.first_name,
                                                                  from_email=EMAIL_HOST_USER, email=queryset.email)
                            user_query = User.objects.get(id=queryset.user.id)
                            user_query.is_recruiter = True
                            user_query.save()
                            serializer.save(updated_at=datetime.now(), active=True)
                        elif not serializer.validated_data.get('active'):
                            RecruiterNotification.denied_recruiter(self=self, recruiter=queryset,
                                                                   recruiter_name=queryset.first_name)
                            for i in Profile.objects.filter(recruiter=queryset):
                                i.active = False
                                i.save()
                            user_query = User.objects.get(id=queryset.user.id)
                            user_query.is_recruiter = False
                            user_query.save()
                            serializer.save(updated_at=datetime.now(), active=False)
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
            instance.active = False
            user_query = User.objects.get(id=instance.user.id)
            RecruiterNotification.denied_recruiter(self=self, recruiter=instance,
                                                   recruiter_name=instance.first_name)
            user_query.is_recruiter = False
            user_query.save()
            instance.save()
            return Response({"Recruiter Deactivated": "Access Granted"}, status=200)
        else:
            return Response({"NO_ACCESS": "Access Denied"}, status=401)
`