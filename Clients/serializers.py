from rest_framework import serializers
from .models import Client

class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ['id', 'first_name', 'last_name', 'phone_number', 'address', 'email', 'status', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

        def validate(self, validated_data):
            validated_data['organization'] = self.context['request'].user.organization

            return super().validate(validated_data)