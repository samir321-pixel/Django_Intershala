from .models import *
from rest_framework import serializers

from student.models import StudentApplication


class ProfileSerializer(serializers.ModelSerializer):
    sallery = serializers.CharField(max_length=200)

    class Meta:
        model = Profile
        fields = '__all__'


class ProfileReadSerializer(serializers.ModelSerializer):
    sallery = serializers.CharField(max_length=200)

    class Meta:
        model = Profile
        fields = '__all__'
        depth = 1


class StudentApplicationReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentApplication
        fields = '__all__'


class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = '__all__'


class AssessmentQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assessment_question
        fields = '__all__'
