from decimal import Decimal

from django.db import transaction

from Ai.models import AIExecution
from Ai.services.proposal_generator import generate_proposal
from Proposals.models import (
    ProposalSection,
    ProposalLineItem,
    ProposalVersion,
    PricingItem,
)


class ProposalAgent:

    def __init__(self, proposal):
        self.proposal = proposal

    @transaction.atomic
    def run(self):

        execution = AIExecution.objects.create(
            organization=self.proposal.organization,
            proposal=self.proposal,
            agent_type=AIExecution.AgentType.PROPOSAL,
            status=AIExecution.Status.RUNNING,
            model_name="gpt-5.6-luna",
        )

        try:

            pricing_catalog = self.get_pricing_catalog()

            result, openai_response = generate_proposal(
                site_walk_notes=self.proposal.note or "",
                pricing_catalog=pricing_catalog,
            )

            self.proposal.sections.all().delete()
            self.proposal.line_items.all().delete()

            self.create_sections(result)

            self.create_line_items(result)

            self.create_version(result)

            self.update_totals()

            execution.output_data = result.model_dump(
                mode="json"
            )

            execution.status = (
                AIExecution.Status.COMPLETED
            )

            execution.save()

            return result

        except Exception as exc:

            execution.status = (
                AIExecution.Status.FAILED
            )

            execution.error_message = str(exc)

            execution.save()

            raise

    def get_pricing_catalog(self):
        return list(
            self.proposal.organization.pricing_items.filter(active=True).values(
                "id",
                "name",
                "description",
                "unit",
                "unit_price",
            )
        )

    def create_sections(self, result):
        for order, section in enumerate(result.sections):
            ProposalSection.objects.create(
                proposal=self.proposal,
                title=section.title,
                content=section.content,
                order=order,
            )

    def create_line_items(self, result):
        pricing_items = self.proposal.organization.pricing_items.filter(
            active=True,
            id__in=[item.pricing_item_id for item in result.line_items],
        )
        pricing_by_id = {item.id: item for item in pricing_items}

        for item in result.line_items:
            pricing_item = pricing_by_id.get(item.pricing_item_id)
            if pricing_item is None:
                raise ValueError(
                    f"Pricing item {item.pricing_item_id} is not available for this organization."
                )

            ProposalLineItem.objects.create(
                proposal=self.proposal,
                pricing_item=pricing_item,
                name=pricing_item.name,
                description=item.reason,
                quantity=item.quantity,
                unit=pricing_item.unit,
                unit_price=pricing_item.unit_price,
                total_price=pricing_item.unit_price * item.quantity,
                ai_suggested=True,
            )

    def create_version(self, result):
        latest_version = self.proposal.versions.order_by("-version_number").first()
        version_number = (latest_version.version_number + 1) if latest_version else 1
        ProposalVersion.objects.create(
            proposal=self.proposal,
            version_number=version_number,
            content=result.model_dump(mode="json"),
            created_by=self.proposal.created_by,
        )

    def update_totals(self):
        subtotal = sum(
            (item.total_price for item in self.proposal.line_items.all()),
            Decimal("0.00"),
        )
        self.proposal.subtotal = subtotal
        self.proposal.total = subtotal + self.proposal.tax
        self.proposal.save(update_fields=["subtotal", "total", "updated_at"])

