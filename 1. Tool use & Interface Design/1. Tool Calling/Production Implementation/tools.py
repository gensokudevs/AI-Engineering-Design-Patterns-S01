import json
from collections.abc import Awaitable, Callable
from dataclasses import dataclass
from typing import Any, Literal

from context import RequestContext
from pydantic import BaseModel, Field, ValidationError
from shopco import orders, payments


class ToolError(Exception):
    """An expected, model-recoverable failure. Message is shown to the model."""


class GetOrderStatusArgs(BaseModel):
    order_id: str = Field(
        pattern=r"^ORD-\d{6}$",
        description="ShopCo order ID, format ORD-###### (e.g. ORD-100234).",
    )


class IssueRefundArgs(BaseModel):
    order_id: str = Field(pattern=r"^ORD-\d{6}$")
    amount_cents: int = Field(
        gt=0, le=50_000,
        description="Refund amount in integer cents. $45.00 = 4500. Max 50000.",
    )
    reason: Literal["damaged", "late", "wrong_item", "not_received"]


async def get_order_status(args: GetOrderStatusArgs, ctx: RequestContext) -> dict:
    order = await orders.get(args.order_id)
    # Ownership check: a hallucinated or someone-else's ID looks identical
    # to a non-existent one. Never leak existence.
    if order is None or order.user_id != ctx.user_id:
        raise ToolError(f"No order {args.order_id} found for this customer.")
    return {
        "order_id": order.id,
        "status": order.status,
        "total_cents": order.total_cents,
        "shipped_at": order.shipped_at.isoformat() if order.shipped_at else None,
    }


async def issue_refund(args: IssueRefundArgs, ctx: RequestContext) -> dict:
    order = await orders.get(args.order_id)
    if order is None or order.user_id != ctx.user_id:
        raise ToolError(f"No order {args.order_id} found for this customer.")
    if args.amount_cents > order.total_cents - order.refunded_cents:
        raise ToolError(
            f"Refund exceeds refundable balance "
            f"({order.total_cents - order.refunded_cents} cents)."
        )
    refund = await payments.refund(
        order_id=order.id,
        amount_cents=args.amount_cents,
        reason=args.reason,
        requested_by=ctx.user_id,
        request_id=ctx.request_id,
        idempotency_key=f"{order.id}:{args.reason}",
    )
    if refund.replayed:
        raise ToolError(
            f"Order {order.id} was already refunded for '{args.reason}' "
            f"(refund {refund.id}). No new refund was issued."
        )
    return {"refund_id": refund.id, "amount_cents": refund.amount_cents,
            "status": refund.status}


@dataclass(frozen=True)
class Tool:
    name: str
    description: str
    args_model: type[BaseModel]
    handler: Callable[[Any, RequestContext], Awaitable[dict]]

    def to_api_schema(self) -> dict:
        return {
            "name": self.name,
            "description": self.description,
            "input_schema": self.args_model.model_json_schema(),
        }


REGISTRY: dict[str, Tool] = {
    t.name: t for t in [
        Tool(
            name="get_order_status",
            description=(
                "Look up the current status, total and ship date of one of the "
                "customer's orders. Use this before discussing any specific order. "
                "Do not guess order details."
            ),
            args_model=GetOrderStatusArgs,
            handler=get_order_status,
        ),
        Tool(
            name="issue_refund",
            description=(
                "Issue a refund on one of the customer's orders. Only call this "
                "after get_order_status confirms the order and the customer's "
                "complaint fits one of the allowed reasons. This moves real money "
                "immediately; never call it for a hypothetical or future refund."
            ),
            args_model=IssueRefundArgs,
            handler=issue_refund,
        ),
    ]
}

TOOL_SCHEMAS = [t.to_api_schema() for t in REGISTRY.values()]


def _result(call_id: str, content: str, is_error: bool = False) -> dict:
    return {"type": "tool_result", "tool_use_id": call_id,
            "content": content, "is_error": is_error}


async def execute_tool_call(block, ctx: RequestContext) -> dict:
    tool = REGISTRY.get(block.name)
    if tool is None: # hallucinated tool
        return _result(block.id, f"Unknown tool '{block.name}'.", is_error=True)

    try:  # malformed / out-of-range args
        args = tool.args_model.model_validate(block.input)
    except ValidationError as e:
        return _result(block.id,
                       f"Invalid arguments: {e.errors(include_url=False)}",
                       is_error=True)

    try:  # expected business failures
        output = await tool.handler(args, ctx)
    except ToolError as e:
        return _result(block.id, str(e), is_error=True)

    return _result(block.id, json.dumps(output))