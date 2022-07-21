from rest_framework import serializers
from .models import CustomUser


class SignupSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('username', 'email')
        model = CustomUser


class ConfCodeSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('username', 'confirmation_code')
        model = CustomUser
