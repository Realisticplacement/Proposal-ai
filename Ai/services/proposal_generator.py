import json

from .openai_client import client
from Ai.prompts.proposal import PROPOSAL_SYSTEM_PROMPT
from Ai.schemas.proposal import ProposalOutput


MODEL = "gpt-5.6-luna"


def generate_proposal(site_walk_notes,pricing_catalog,):

    prompt = f"""SITE WALK NOTES================
{site_walk_notes}

PRICING CATALOG================
{json.dumps(pricing_catalog, default=str)}"""

    response = client.responses.create(
        model=MODEL,
        instructions=PROPOSAL_SYSTEM_PROMPT,
        input=prompt,
        text={
            "format": {
                "type": "json_schema",
                "name": "proposal_output",
                "schema": ProposalOutput.model_json_schema(),
                "strict": True,
            }
        },
    )

    raw_output = response.output_text

    proposal = ProposalOutput.model_validate_json(
        raw_output
    )

    return proposal, response