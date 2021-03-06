from user.models import User
from .models import *
from rest_framework.response import Response
from .serializers import *
from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated


# Create your views here.
class CreateRecruiter(viewsets.ModelViewSet):
    queryset = Recruiter.objects.all()
    serializer_class = RecruiterSerializer
    lookup_field = "id"


class RecruiterNotificationViewSets(generics.ListAPIView):
    queryset = RecruiterNotification.objects.all().order_by('-created_at')
    serializer_class = RecruiterNotificationSerializers
    permission_classes = [IsAuthenticated,]

    def list(self, request, *args, **kwargs):
        if self.request.user.is_recruiter:
            queryset = RecruiterNotification.objects.filter(
                recruiter=Recruiter.objects.get(user=self.request.user.id)).order_by('-created_at')
            queryset.update(seen=True)
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data, status=200)
        else:
            return Response({"NO_ACCESS": "Access Denied"}, status=401)
