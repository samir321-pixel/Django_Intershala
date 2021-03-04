from rest_framework import serializers
from .models import *
from student.models import Student


class IntershalaStudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'
