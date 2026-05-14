from rest_framework import serializers

from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id', 'email', 'first_name', 'last_name', 'phone_number',
            'user_type', 'is_verified', 'subscription_plan', 'profile_photo',
            'date_joined',
        ]
        read_only_fields = ['id', 'date_joined', 'is_verified']


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    password_confirm = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            'email', 'password', 'password_confirm', 'first_name',
            'last_name', 'phone_number', 'user_type', 'id_number',
        ]

    def validate(self, data):
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError({'password_confirm': 'Passwords do not match.'})
        return data

    def create(self, validated_data):
        validated_data.pop('password_confirm')
        return User.objects.create_user(**validated_data)


class UserMinimalSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='full_name', read_only=True)

    class Meta:
        model = User
        fields = ['id', 'name', 'phone_number', 'email']
