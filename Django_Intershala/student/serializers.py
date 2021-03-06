from .models import Student
from rest_framework import serializers
from .models import *
from job_profile.models import Profile


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = "__all__"


class StudentApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentApplication
        fields = "__all__"


class JobProfileReadSerializer(serializers.ModelSerializer):
    sallery = serializers.CharField(max_length=200)

    class Meta:
        model = Profile
        fields = "__all__"
        depth = 1
