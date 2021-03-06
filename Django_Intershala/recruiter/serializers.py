from .models import Recruiter
from rest_framework import serializers

from .notification_models import RecruiterNotification


class RecruiterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recruiter
        fields = '__all__'


class RecruiterNotificationSerializers(serializers.ModelSerializer):
    class Meta:
        model = RecruiterNotification
        fields = '__all__'


