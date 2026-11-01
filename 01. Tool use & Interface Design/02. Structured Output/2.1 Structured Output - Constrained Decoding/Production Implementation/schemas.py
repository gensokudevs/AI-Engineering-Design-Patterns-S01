from enum import StrEnum
from typing import Annotated, Any

from anthropic import transform_schema
from pydantic import BaseModel, ConfigDict, Field, field_validator


class Category(StrEnum):
    """Which team owns the ticket."""
    BILLING = "billing"
    SHIPPING = "shipping"
    PRODUCT = "product"
    ACCOUNT = "account"
    OTHER = "other"


class Priority(StrEnum):
    """critical: money lost, account locked, legal or safety risk.
    high: order blocked or customer explicitly time-pressed.
    normal: standard issue with a clear path. low: questions, feedback."""
    CRITICAL = "critical"
    HIGH = "high"
    NORMAL = "normal"
    LOW = "low"


class Sentiment(StrEnum):
    """Customer's emotional tone."""
    POSITIVE = "positive"
    NEUTRAL = "neutral"
    NEGATIVE = "negative"


OrderId = Annotated[str, Field(pattern=r"^ORD-\d{6}$")]


class TicketTriage(BaseModel):
    """The contract between the model and the routing code.
    Field order is generation order: evidence first, decisions after."""

    # The docstrings above (this one and each enum's) are sent to the model as part of the
    # schema, so editing them changes the prompt.
    model_config = ConfigDict(extra="forbid", frozen=True)

    evidence: str = Field(
        max_length=300,
        description="One or two sentences quoting the facts in the ticket that the fields "
        "below rely on.",
    )
    category: Category
    priority: Priority
    sentiment: Sentiment
    order_ids: list[OrderId] = Field(
        description="Order IDs that appear verbatim in the ticket. Empty list if none. "
        "Never invent or complete partial IDs.",
    )
    requires_human: bool = Field(
        description="True for legal threats, chargebacks, safety issues, "
        "or anything you cannot triage confidently.",
    )
    summary: str = Field(max_length=280, description="One sentence for the agent picking this up.")

    @field_validator("category", "priority", "sentiment", mode="before")
    @classmethod
    def lowercase_enums(cls, value: Any) -> Any:
        # The API guarantees the enum's spelling but not its case, so "Shipping" can come back.
        return value.strip().lower() if isinstance(value, str) else value


# Constraints that anthropic's API doesn't support (like max_length) are moved into
# the descriptions; Pydantic still enforces them when we validate the reply.
TRIAGE_SCHEMA: dict[str, Any] = transform_schema(TicketTriage)
# {
#   "type": "integer",
#   "minimum": 1,
#   "maximum": 10,
#   "description": "A number",
# }
# {'type': 'integer', 'description': 'A number {minimum: 1, maximum: 10}'}