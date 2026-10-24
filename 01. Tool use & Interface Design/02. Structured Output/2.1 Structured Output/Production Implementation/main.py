"""Offline. Prints the schema the model receives, then shows what the validation layer
does with the drift the naive version let through. Run: python main.py"""
import json
from typing import Any

from pydantic import ValidationError
from schemas import TRIAGE_SCHEMA, TicketTriage

VALID: dict[str, Any] = {
    "evidence": "Customer says the parcel for ORD-100234 never arrived.",
    "category": "shipping", "priority": "high", "sentiment": "negative",
    "order_ids": ["ORD-100234"], "requires_human": False, "summary": "Parcel lost.",
}
CASES: dict[str, dict[str, Any]] = {
    "Casing drift (the documented API caveat)": {"category": "Shipping"},
    "Synonym instead of enum value": {"priority": "urgent"},
    "Extra / renamed key": {"priority_level": "high"},
    "String instead of list": {"order_ids": "ORD-100234, ORD-100235"},
    "Invented order id": {"order_ids": ["12345"]},
    "Over-long summary": {"summary": "x" * 3000},
}


def main() -> None:
    print("=== Wire schema sent in output_config.format")
    print(json.dumps(TRIAGE_SCHEMA, indent=2))
    for name, patch in CASES.items():
        try:
            triage = TicketTriage.model_validate_json(json.dumps(VALID | patch))
            print(f"\n{name}: ACCEPTED -> category={triage.category!r}")
        except ValidationError as exc:
            err = exc.errors(include_url=False, include_input=False)[0]
            print(f"\n{name}: REJECTED -> {err['loc']}: {err['msg']}")


if __name__ == "__main__":
    main()
