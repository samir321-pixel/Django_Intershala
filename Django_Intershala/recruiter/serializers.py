from .models import *
from rest_framework import serializers

from .notification_models import RecruiterNotification


class RecruiterSignINSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recruiter
        fields = ['first_name', 'last_name', 'email', 'company', 'DOB', 'gender', 'company_address', 'city', 'state',
                  'password', 'pincode', ]


class RecruiterProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recruiter
        fields = '__all__'


class RecruiterReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecruiterReview
        fields = '__all__'


class RecruiterNotificationSerializers(serializers.ModelSerializer):
    class Meta:
        model = RecruiterNotification
        fields = '__all__'
