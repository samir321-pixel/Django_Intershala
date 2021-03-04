from rest_framework import serializers
from .models import *
from student.models import Student
from recruiter.models import Recruiter


class IntershalaStudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'
        depth = 2


class IntershalaRecruiterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recruiter
        fields = '__all__'
        depth = 2
