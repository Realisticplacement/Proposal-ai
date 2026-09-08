from django.shortcuts import render
from django.utils import timezone

from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Proposal
from .serializers import ProposalSerializer
from .permissions import IsProposalOrganizationMember




# Create your views here.
class ProposalViewset(viewsets.ModelViewSet):

    serializer_class = ProposalSerializer

    permission_classes = [IsAuthenticated,IsProposalOrganizationMember,]

    def get_queryset(self):

        return Proposal.objects.filter(organization=self.request.user.organization).prefetch_related("sections", "line_items","versions",)

    def perform_create(self, serializer):

        serializer.save(organization=self.request.user.organization,created_by=self.request.user,)

    @action(detail=True, methods=["post"])

    def approve(self, request, pk=None):

        proposal = self.get_object()

        if proposal.status != Proposal.Status.REVIEW:
            return Response(
                {
                    "detail": ("Only proposals in review ""can be approved.")
                },
                status=status.HTTP_400_BAD_REQUEST,
                )

        proposal.status = Proposal.Status.APPROVED

        proposal.approved_by = request.user

        proposal.approved_at = timezone.now()

        proposal.save()

        return Response(
            ProposalSerializer(proposal).data
        )
