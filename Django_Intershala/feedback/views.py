from rest_framework import generics, viewsets
from rest_framework.permissions import IsAuthenticated
from .serializers import *
from .models import *
from rest_framework.response import Response


class FeedBackViewsets(generics.CreateAPIView):
    queryset = IntershalaFeedBack.objects.all()
    serializer_class = FeedbackSerializer
    permission_classes = (IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=self.request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(user=self.request.user)
            return Response(serializer.data, status=200)
        else:
            return Response(serializer.errors, status=401)


class AllFeedBackViewSets(generics.ListAPIView):
    queryset = IntershalaFeedBack.objects.all()
    serializer_class = FeedbackReadSerializer
    permission_classes = (IsAuthenticated,)

    def list(self, request, *args, **kwargs):
        if self.request.user.is_admin or self.request.user.is_employee or self.request.user.is_superuser:
            queryset = IntershalaFeedBack.objects.all().order_by('-created_at')
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data, status=200)
        else:
            return Response({"NO_ACCESS": "Access Denied"}, status=401)
