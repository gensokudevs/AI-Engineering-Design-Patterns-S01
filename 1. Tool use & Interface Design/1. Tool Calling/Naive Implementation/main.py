"""Replays realistic model outputs through the naive parser and executor.
The signed-in customer is u_1. No API key needed. Run: python demo_failures.py"""
import asyncio

from agent import parse_action, run_lookup, run_refund

CASES = {
    "1. Conditional language fires now":
        "Once you've shipped the item back, I'll process REFUND: ORD-100235 $45.10 for you.",
    "2. Negation fires anyway":
        "I can't do REFUND: ORD-100234 $50 because it's outside the 30-day window.",
    "3. Thousands separator ($1,200.00)":
        "Approved. REFUND: ORD-100234 $1,200.00",
    "4. Sentence-ending period":
        "Done! I've issued REFUND: ORD-100235 $45.10.",
    "5. Markdown bold around the marker":
        "Let me check that. **LOOKUP_ORDER:** ORD-100234",
    "6. Near-miss syntax leaks to the customer":
        "REFUND: ORD-100235 forty-five dollars",
    "7. Someone else's order (owned by u_2)":
        "LOOKUP_ORDER: ORD-200001",
    "8. Two actions, one silently dropped":
        "LOOKUP_ORDER: ORD-100235\nREFUND: ORD-100235 $45.10",
    "9. Hallucinated order ID":
        "REFUND: ORD-999999 $20",
}

async def main() -> None:
    for name, raw in CASES.items():
        print(f"\n=== {name}")
        try:
            action = parse_action(raw)
            print(f"  parsed -> {action}")
            match action.kind:
                case "refund":
                    print(f"  EXECUTED: {await run_refund(action)}")
                case "lookup":
                    print(f"  LOOKUP RESULT: {await run_lookup(action)}")
                case _:
                    print(f"  SENT TO CUSTOMER VERBATIM: {raw!r}")
        except (ValueError, KeyError, TypeError) as exc:
            print(f"  CRASH -> HTTP 500 ({type(exc).__name__}: {exc})")

if __name__ == "__main__":
    asyncio.run(main())