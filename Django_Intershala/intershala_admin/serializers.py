from rest_framework import serializers
from .models import *
from student.models import Student
from recruiter.models import Recruiter
from job_profile.models import Profile, Skill

from job_profile.serializers import ProfileReadSerializer


class IntershalaAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = IntershalaAdmin
        fields = '__all__'


class CompanyReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyReview
        fields = '__all__'


class IntershalaCompanyWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = IntershalaCompany
        fields = '__all__'


class IntershalaCompanyReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = IntershalaCompany
        fields = '__all__'
        depth = 1


class IntershalaStudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'
        depth = 2


class IntershalaEmployeeSerializer(serializers.ModelSerializer):
    salary = serializers.CharField(max_length=200)

    class Meta:
        model = IntershalaEmployee
        fields = '__all__'


class AdminNotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdminNotification
        fields = '__all__'
        depth = 1


class EmployeeNotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeNotification
        fields = '__all__'
        depth = 1


class IntershalaRecruiterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recruiter
        fields = '__all__'


class IntershalaJobProfileReadSerializer(serializers.ModelSerializer):
    sallery = serializers.CharField(max_length=200)

    class Meta:
        model = Profile
        fields = '__all__'


class IntershalaSkillReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = '__all__'
        depth = 1


class IntershalaWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = '__all__'
