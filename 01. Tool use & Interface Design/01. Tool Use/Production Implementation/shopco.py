import uuid
from dataclasses import dataclass, replace
from datetime import datetime, timezone


@dataclass
class Order:
    id: str
    user_id: str
    status: str
    total_cents: int
    refunded_cents: int
    shipped_at: datetime | None


@dataclass
class Refund:
    id: str
    amount_cents: int
    status: str
    replayed: bool = False   # True when an idempotency key matched an earlier refund

_FAKE_ORDERS = {
    "ORD-100234": Order("ORD-100234", "u_1", "delivered", 4500, 0,
                        datetime(2026, 9, 10, tzinfo=timezone.utc)),
    "ORD-100235": Order("ORD-100235", "u_1", "processing", 12000, 0, None),
    "ORD-200001": Order("ORD-200001", "u_2", "delivered", 9900, 0,
                        datetime(2026, 9, 1, tzinfo=timezone.utc)),
}


class _Orders:
    async def get(self, order_id):
        # Returns the Order, or None if it doesn't exist.
        return _FAKE_ORDERS.get(order_id)


class _Payments:
    def __init__(self):
        self._by_key = {}   # idempotency_key -> the Refund it produced

    async def refund(self, order_id, amount=None, amount_cents=None,
                     reason=None, requested_by=None, request_id=None,
                     idempotency_key=None):
        # Same key again -> hand back the original refund, move no money.
        if idempotency_key in self._by_key:
            return replace(self._by_key[idempotency_key], replayed=True)
        
        if amount_cents is None:
            amount_cents = int(float(amount) * 100)

        print(f"[FAKE PAYMENT] Refunding {amount_cents} cents on {order_id} "
              f"(reason={reason}, by={requested_by}, request={request_id})")
        
        order = _FAKE_ORDERS.get(order_id)

        if order:
            order.refunded_cents += amount_cents

        refund = Refund(id=f"RF-{uuid.uuid4().hex[:8]}",
                        amount_cents=amount_cents, status="completed")
        
        if idempotency_key is not None:
            self._by_key[idempotency_key] = refund

        return refund

orders = _Orders()
payments = _Payments()
