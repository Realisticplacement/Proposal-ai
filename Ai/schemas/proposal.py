from pydantic import BaseModel, ConfigDict, Field

class ProposalLineItemOutput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    pricing_item_id: int
    quantity: int = Field(ge=1)
    reason: str


class ProposalSectionOutput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    title: str
    content: str


class ProposalOutput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    project_summary: str

    sections: list[ProposalSectionOutput]

    line_items: list[ProposalLineItemOutput]

    missing_information: list[str]

    assumptions: list[str]