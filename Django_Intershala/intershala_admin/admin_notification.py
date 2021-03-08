from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .serializers import *
# Create your views here.
from rest_framework.response import Response
from django.core.exceptions import ObjectDoesNotExist


class AdminNotificationViewsets(generics.ListAPIView, generics.RetrieveAPIView):
    serializer_class = AdminNotificationSerializer
    queryset = AdminNotification.objects.all().order_by('-created_at')
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        if self.request.user.is_admin or self.request.user.is_superuser or self.request.user.is_employee:
            queryset = AdminNotification.objects.all().order_by('-created_at')
            for i in queryset:
                i.seen = True
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data, status=200)

    def retrieve(self, request, *args, **kwargs):
        if self.request.user.is_admin or self.request.user.is_superuser or self.request.user.is_employee:
            queryset = AdminNotification.objects.get(id=self.kwargs["id"])
            serializer = self.get_serializer(queryset)
            return Response(serializer.data, status=200)
