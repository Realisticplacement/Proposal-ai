from typing import cast

from Accounts.models import User
from django.db import OperationalError
from django.db.models import QuerySet
from django.utils import timezone

from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Proposal
from .serializers import ProposalSerializer
from .permissions import IsProposalOrganizationMember
from Ai.Agent.proposal_agent import ProposalAgent




# Create your views here.
class ProposalViewset(viewsets.ModelViewSet):

    serializer_class = ProposalSerializer

    permission_classes = [IsAuthenticated,IsProposalOrganizationMember,]

    def get_queryset(self) -> QuerySet[Proposal]:  # pyright: ignore[reportIncompatibleMethodOverride]

        user = cast(User, self.request.user)
        if user.organization is None:
            return Proposal.objects.none()
        return Proposal.objects.filter(organization=user.organization).prefetch_related("sections", "line_items", "versions")

    def perform_create(self, serializer):

        user = cast(User, self.request.user)
        if user.organization is None:
            raise PermissionDenied('You must belong to an organization to create a proposal.')
        serializer.save(organization=user.organization, created_by=user)

    @action(
    detail=True,
    methods=["post"],
)
    def approve(self, request, pk=None):
        proposal = self.get_object()

        if proposal.status != Proposal.Status.REVIEW:
            return Response({"detail": ("Only proposals in REVIEW ""can be approved.")},
                status=status.HTTP_400_BAD_REQUEST,
            )

        proposal.status = Proposal.Status.APPROVED
        proposal.approved_by = request.user
        proposal.approved_at = timezone.now()

        proposal.save(update_fields=["status","approved_by","approved_at",])

        return Response({"status": "approved","proposal_id": proposal.id,})

    @action(detail=True,methods=["post"],)
    def generate(self, request, pk=None):

        proposal = self.get_object()

        if proposal.status not in [
            Proposal.Status.SITE_WALK_DATA,
            Proposal.Status.CHANGES_REQUESTED,
        ]:
            return Response({"detail": ("This proposal cannot be generated ""in its current state.")},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            proposal.status = Proposal.Status.PROCESSING
            proposal.save(update_fields=["status"])

            result = ProposalAgent(proposal).run()
            proposal.status = Proposal.Status.DRAFT
            proposal.save(update_fields=["status"])

            return Response({"status": "success", "proposal_id": proposal.id, "result": result.model_dump(mode="json")},
                status=status.HTTP_200_OK,
            )

        except OperationalError:
            return Response({ "status": "error","detail": "The database is temporarily unavailable. Please retry shortly.",},
                status=status.HTTP_503_SERVICE_UNAVAILABLE,
            )

        except Exception as exc:
            try:
                proposal.status = Proposal.Status.SITE_WALK_DATA
                proposal.save(update_fields=["status"])
            except OperationalError:
                return Response(
                    {
                        "status": "error",
                        "detail": "The database is temporarily unavailable. Please retry shortly.",
                    },
                    status=status.HTTP_503_SERVICE_UNAVAILABLE,
                )

            return Response(
                {"status": "error","detail": str(exc),},status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
