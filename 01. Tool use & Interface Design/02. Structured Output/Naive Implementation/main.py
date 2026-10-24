"""Replays realistic model outputs through the naive parser and router.
No API key needed. Run: python demo_failures.py"""
from triage import parse_triage, route

CASES = {
    "1. Preamble containing braces":
        'Triage for {ticket #8812}:\n{"category": "shipping", "priority": "P1", '
        '"sentiment": "negative", "order_ids": ["ORD-100234"], "requires_human": false, '
        '"summary": "Package lost."}',
    "2. Trailing comma":
        '{"category": "billing", "priority": "P2", "sentiment": "negative", '
        '"order_ids": [], "requires_human": false, "summary": "Double charge.",}',
    "3. Truncated at max_tokens (was a P1)":
        '{"category": "billing", "priority": "P1", "sentiment": "negative", '
        '"order_ids": ["ORD-100234"], "requires_hu',
    "4. Casing + synonym drift":
        '{"category": "Billing", "priority": "urgent", "sentiment": "negative", '
        '"order_ids": [], "requires_human": false, "summary": "Charged twice."}',
    "5. Renamed key + string boolean":
        '{"category": "shipping", "priority_level": "P1", "sentiment": "neutral", '
        '"order_ids": [], "requires_human": "false", "summary": "Where is my parcel?"}',
    "6. String instead of list":
        '{"category": "shipping", "priority": "P2", "sentiment": "neutral", '
        '"order_ids": "ORD-100234, ORD-100235", "requires_human": false, '
        '"summary": "Two late orders."}',
    "7. Prose instead of JSON":
        "I'm not able to categorise this message confidently.",
    "8. Valid JSON, invalid values":
        '{"category": "shipping", "priority": "P1", "sentiment": "furious", '
        '"order_ids": ["12345"], "requires_human": false, "summary": "' + "x" * 3000 + '"}',
}

for name, raw in CASES.items():
    print(f"\n=== {name}")
    try:
        rec = route("demo", parse_triage(raw))
    except (ValueError, TypeError, KeyError) as exc:
        print(f"  CRASH -> HTTP 500, ticket lost ({type(exc).__name__})")
        continue
    ids = rec["order_ids"]
    print(
        f"  queue={rec['queue']!r} priority={rec['priority']!r} sla={rec['sla_hours']}h "
        f"order_ids={ids!r} (downstream count: {len(ids)}) summary_len={len(rec['summary'])}"
    )