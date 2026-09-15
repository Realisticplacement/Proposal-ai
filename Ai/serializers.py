from rest_framework import serializers
from .models import AIExecution


class AIExecutionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AIExecution
        fields = ['id', 'agent_type', 'status', 'model_name', 'organization', 'token_used', 'input_data', 'output_data', 'error_message', 'started_at', 'completed_at', 'created_at']
        read_only_fields = ['id', 'status', 'model_name', 'organization', 'token_used', 'output_data', 'error_message', 'started_at', 'completed_at', 'created_at']