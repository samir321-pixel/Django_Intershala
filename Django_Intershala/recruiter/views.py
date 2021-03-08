from user.models import User
from .models import *
from rest_framework.response import Response
from .serializers import *
from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated
from django.db import IntegrityError

from intershala_admin.models import AdminNotification


class RecruiterSignin(generics.CreateAPIView):
    queryset = Recruiter.objects.all()
    serializer_class = RecruiterSignINSerializer

    def perform_create(self, serializer):
        try:
            user = User.objects.create_user(username=self.request.data['first_name'],
                                            password=self.request.data['password'],
                                            email=self.request.data['email'],
                                            is_recruiter=False)
        except IntegrityError:
            return Response({"RECRUITER_EXISTS": "Recruiter already exists with this Email."}, status=400)
        serializer = self.get_serializer(data=self.request.data)
        if serializer.is_valid(raise_exception=True):
            data = serializer.save(user=user, active=False)
            recruiter_query = Recruiter.objects.get(id=data.id)
            if data:
                AdminNotification.notify_admin(recruiter=recruiter_query,
                                               recruiter_name=self.request.data.get('first_name'))
            return Response(serializer.data, status=200)
        else:
            return Response(serializer.errors, status=400)


class RecruiterNotificationViewSets(generics.ListAPIView):
    queryset = RecruiterNotification.objects.all().order_by('-created_at')
    serializer_class = RecruiterNotificationSerializers
    permission_classes = [IsAuthenticated, ]

    def list(self, request, *args, **kwargs):
        if self.request.user.is_recruiter:
            queryset = RecruiterNotification.objects.filter(
                recruiter=Recruiter.objects.get(user=self.request.user.id)).order_by('-created_at')
            queryset.update(seen=True)
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data, status=200)
        else:
            return Response({"NO_ACCESS": "Access Denied"}, status=401)
