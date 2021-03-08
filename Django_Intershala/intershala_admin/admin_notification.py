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

    def list(self, request, *args, **kwargs):
        if self.request.user.is_admin or self.request.user.is_superuser or self.request.user.is_employee:
            serializer = self.get_serializer(self.queryset, many=True)
            return Response(serializer.data, status=200)
