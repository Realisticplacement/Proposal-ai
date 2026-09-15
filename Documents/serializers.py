from rest_framework import serializers
from Clients.models import Client
from Proposals.models import Proposal

from .models import Document

class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ['id', 'name', 'document_type', 'file', 'client', 'proposal','extracted_text', 'metadata', 'created_at']
        read_only_fields = ['id', 'extracted_text', 'created_at']

    def validate_file(self, file):
        max_size = 10 * 1024 * 1024
        if file is not None and file.size > max_size:
            raise serializers.ValidationError('Files must be 10 MB or smaller.')
        return file

    def validate(self, attrs):
        organization = self.context['request'].user.organization
        client = attrs.get('client')
        proposal = attrs.get('proposal')

        if client is not None and not Client.objects.filter(
            pk=client.pk,
            organization=organization,
        ).exists():
            raise serializers.ValidationError({
                'client': 'The client must belong to your organization.'
            })

        if proposal is not None and not Proposal.objects.filter(
            pk=proposal.pk,
            organization=organization,
        ).exists():
            raise serializers.ValidationError({
                'proposal': 'The proposal must belong to your organization.'
            })

        return attrs

