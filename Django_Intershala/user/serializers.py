from allauth.account.adapter import get_adapter
from rest_auth.registration.serializers import RegisterSerializer
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from . import models


class CoreRegisterSerializer(RegisterSerializer):
    is_admin = serializers.BooleanField(default=False)
    is_employee = serializers.BooleanField(default=False)
    is_customer = serializers.BooleanField(default=False)

    class Meta:
        model = models.User
        fields = ('email', 'username', 'password', 'is_admin', 'is_employee', 'is_customer', 'first_name')

    def get_cleaned_data(self):
        return {
            'username': self.validated_data.get('username', ''),
            'email': self.validated_data.get('email', ''),
            'first_name': self.validated_data.get('first_name', ''),
            'password1': self.validated_data.get('password1', ''),
            'password2': self.validated_data.get('password2', ''),
            'is_admin': self.validated_data.get('is_admin', ''),
            'is_employee': self.validated_data.get('is_employee', ''),
            'is_customer': self.validated_data.get('is_customer', ''),
        }

    def save(self, request):
        adapter = get_adapter()
        user = adapter.new_user(request)
        self.cleaned_data = self.get_cleaned_data()
        user.is_admin = self.cleaned_data.get('is_admin')
        user.is_employee = self.cleaned_data.get('is_employee')
        user.is_customer = self.cleaned_data.get('is_customer')
        user.first_name = self.cleaned_data.get('first_name')
        user.save()
        adapter.save_user(request, user, self)
        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = ('email', 'username', 'password', 'is_admin', 'is_employee', 'is_customer', 'first_name')


class ChangePasswordSerializer(serializers.Serializer):
    model = models.User
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)


class TokenSerializer(serializers.ModelSerializer):
    user_type = serializers.SerializerMethodField()

    class Meta:
        model = Token
        fields = ('key', 'user', 'user_type')

    def get_user_type(self, obj):
        serializer_data = UserSerializer(
            obj.user
        ).data
        is_admin = serializer_data.get('is_admin')
        is_employee = serializer_data.get('is_employee')
        is_customer = serializer_data.get('is_customer')

        return {
            'is_admin': is_admin,
            'is_employee': is_employee,
            'is_customer': is_customer,
        }