from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .serializers import *
# Create your views here.
from student.models import Student


class IntershalaStudentViewSets(viewsets.ModelViewSet):
    queryset = Student.objects.all().order_by('-created_at')
    serializer_class = IntershalaStudentSerializer
    permission_classes = (IsAuthenticated,)
    lookup_field = "id"
