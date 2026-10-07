import re
from dataclasses import dataclass
from typing import Literal

from shopco import Order, orders, payments

SYSTEM_PROMPT = """You are a support agent for ShopCo.
If you need an order's status, write exactly: LOOKUP_ORDER: <order_id>
If a refund is warranted, write exactly: REFUND: <order_id> <amount>
Otherwise, just answer the customer."""

LOOKUP_RE = re.compile(r"LOOKUP_ORDER:\s*(\S+)")
REFUND_RE = re.compile(r"REFUND:\s*(\S+)\s+\$?([\d.]+)")

@dataclass(frozen=True)
class Action:
    kind: Literal["refund", "lookup", "reply"]
    order_id: str | None = None
    amount: float | None = None

def parse_action(text: str) -> Action:
    """Scan model prose for command markers."""
    if m := REFUND_RE.search(text):
        return Action("refund", m.group(1), float(m.group(2)))
    if m := LOOKUP_RE.search(text):
        return Action("lookup", m.group(1))
    return Action("reply")

async def run_refund(action: Action) -> str:
    refund = await payments.refund(action.order_id, amount=action.amount)
    return f"Refund of ${refund.amount_cents / 100:.2f} issued for {action.order_id}."

async def run_lookup(action: Action) -> Order | None:
    return await orders.get(action.order_id)