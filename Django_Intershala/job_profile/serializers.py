from .models import *
from rest_framework import serializers

from student.models import StudentApplication


class ProfileSerializer(serializers.ModelSerializer):
    sallery = serializers.CharField(max_length=200)

    class Meta:
        model = Profile
        fields = '__all__'


class AssessmentAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assessment_answer
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


class AssessmentWriteQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assessment_question
        fields = '__all__'


class AssessmentReadQuestionSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()

    class Meta:
        model = Assessment_question
        fields = '__all__'
        depth = 0
