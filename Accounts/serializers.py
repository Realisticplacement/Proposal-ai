from typing import cast

from django.core.exceptions import ValidationError as DjangoValidationError
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import Organization, User


class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = ['id', 'name', 'email', 'created_at', 'updated_at']

        read_only_fields = ['id', 'created_at']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'organization', 'first_name', 'last_name']

        read_only_fields = ['id', 'organization']


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    password_confirm = serializers.CharField(write_only=True)
    organization = serializers.CharField(write_only=True, min_length=1)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'password_confirm', 'first_name', 'last_name', 'organization']
        read_only_fields = ['id']

    def validate(self, attrs):
        if attrs['password'] != attrs.pop('password_confirm'):
            raise serializers.ValidationError({'password_confirm': 'Passwords do not match.'})
        try:
            validate_password(attrs['password'])
        except DjangoValidationError as exc:
            raise serializers.ValidationError({'password': exc.messages}) from exc
        organization_name = attrs['organization'].strip()
        if not organization_name:
            raise serializers.ValidationError({'organization': 'Organization name is required.'})
        if Organization.objects.filter(name__iexact=organization_name).exists():
            raise serializers.ValidationError(
                {'organization': 'This organization already exists. Ask an administrator for an invitation.'}
            )
        attrs['organization'] = organization_name
        return attrs

    def create(self, validated_data):
        organization_name = validated_data.pop('organization')
        organization = Organization.objects.create(name=organization_name)
        validated_data['organization'] = organization
        return User.objects.create_user(**validated_data)


class LoginSerializer(TokenObtainPairSerializer):
    organization = serializers.CharField(write_only=True, min_length=1)

    def validate(self, attrs):
        organization_name = attrs['organization'].strip()
        organization = Organization.objects.filter(name__iexact=organization_name).first()
        if organization is None:
            raise serializers.ValidationError({'organization': 'Organization not found.'})

        data = super().validate(attrs)

        user = cast(User, self.user)
        if user.organization != organization:
            raise serializers.ValidationError(
                'These credentials do not belong to the selected organization.'
            )

        return data