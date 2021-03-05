from rest_framework import viewsets
from .models import *
from .serializers import *
from rest_framework.response import Response


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileReadSerializer
    lookup_field = "id"

    def list(self, request, *args, **kwargs):
        if self.request.user.is_recruiter:
            query = Profile.objects.filter(recruiter=self.request.user).order_by('-created_at')
            serializer = ProfileReadSerializer(query, many=True)
            return Response(serializer.data)
        else:
            return Response({"NO_ACCESS": "Access Denied"}, status=401)

    def perform_create(self, serializer):
        try:
            if self.request.user.is_recruiter:
                serializer = ProfileWriteSerializer(data=self.request.data)
                if serializer.is_valid(raise_exception=True):
                    serializer.save(recruiter=self.request.user)
                return Response(serializer.data, status=200)
        except:
            return Response({"NO_ACCESS": "Access Denied"}, status=401)
