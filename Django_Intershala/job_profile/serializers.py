from .models import *
from rest_framework import serializers


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'


class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = '__all__'


class AssessmentQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assessment_question
        fields = '__all__'
