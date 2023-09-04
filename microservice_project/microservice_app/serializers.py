from rest_framework import serializers
from .models import customUser

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = customUser
        fields =('first_name', 'last_name', 'email', 'phone_number', 'password')
        extra_kwargs= {'password':{'write_only':True}}

class PasswordResetSerializer(serializers.Serializer):
        email = serializers.EmailField()

class AccountUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = customUser
        fields = ['first_name', 'last_name', 'phone_number', 'password']


