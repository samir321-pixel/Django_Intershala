from rest_framework import serializers
from .models import *


class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = IntershalaFeedBack
        fields = '__all__'


class FeedbackReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = IntershalaFeedBack
        fields = "__all__"
        depth = 1
