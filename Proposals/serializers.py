from rest_framework import serializers
from Clients.models import Client
from .models import (Proposal, ProposalSection, ProposalLineItem, ProposalVersion)


class ProposalSectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProposalSection
        fields = ['id', 'title', 'content', 'order']

        read_only_fields = ['id']



class ProposalLineItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProposalLineItem
        fields = ['id', 'name', 'description', 'quantity', 'unit', 'unit_price', 'total_price', 'source_reference', 'ai_suggested']

        read_only_fields = ['id', 'total_price','ai_suggested']



class ProposalVersionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProposalVersion
        fields = ['id', 'version_number', 'content', 'created_by', 'created_at']

        read_only_fields = ['id', 'created_by', 'created_at']



class ProposalSerializer(serializers.ModelSerializer):
    sections = ProposalSectionSerializer(many=True, read_only=True)
    line_items = ProposalLineItemSerializer(many=True, read_only=True)
    versions = ProposalVersionSerializer(many=True, read_only=True)

    class Meta:
        model = Proposal
        fields = ['id', 'title', 'client', 'status', 'note', 'subtotal', 'tax', 'total', 'created_by', 'approved_by', 'approved_at', 'sent_at', 'created_at', 'updated_at', 'sections', 'line_items', 'versions']

        read_only_fields = ['id', 'status', 'subtotal', 'tax', 'total', 'created_by', 'approved_by', 'approved_at', 'sent_at', 'created_at', 'updated_at']
        extra_kwargs = {'client': {'required': True, 'allow_null': False}}

    def validate_client(self, client):
        organization = self.context['request'].user.organization
        if not Client.objects.filter(pk=client.pk, organization=organization).exists():
            raise serializers.ValidationError('The client must belong to your organization.')
        return client
