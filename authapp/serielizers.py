from typing import Any, Dict
from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from .utils import generate_access_token, generate_refresh_token
from rest_framework.exceptions import ValidationError, AuthenticationFailed


User = get_user_model()


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'password', 'first_name', 'username',
                  'last_name', 'role', 'phone']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        role = validated_data.get('role')
        phone = validated_data.get('phone', "")

        print(role, phone)

        if phone == "" and role == 'teacher':
            print('phone number is required')
            raise ValidationError('Phone number is required for Teacher role')

        user = User.objects.create_user(**validated_data)

        if role == 'teacher':
            user.is_staff = True
            user.save()

        if role == 'admin':
            user.is_staff = True
            user.is_superuser = True
            user.save()

        return user


class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'first_name',
                  'last_name', 'role', 'phone']
        read_only_fields = ['id', 'email',
                            'first_name', 'last_name', 'role', 'phone']


class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    class Meta:
        model = User
        fields = ['email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, attrs: Dict[str, Any]) -> Dict[Any, Any]:
        authentication_kwargs = {
            'email': attrs.get('email'),
            'password': attrs.get('password')
        }

        try:
            authentication_kwargs['request'] = self.context.get('request')
        except Exception as e:
            pass

        self.user = authenticate(**authentication_kwargs)

        if self.user is None:
            raise AuthenticationFailed('User with given credentials not found')

        data = {
            'access': generate_access_token(self.user),
            'refresh': generate_refresh_token(self.user)
        }

        return data


class CustomTokenPairSerializer(serializers.BaseSerializer):
    access = serializers.CharField()
    refresh = serializers.CharField()

    def to_representation(self, instance):
        return {
            'access': instance['access'],
            'refresh': instance['refresh']
        }

    def to_internal_value(self, data):
        return {
            'access': data['access'],
            'refresh': data['refresh']
        }

    # def create(self, validated_data):
        # validated_data['access'] = generate
