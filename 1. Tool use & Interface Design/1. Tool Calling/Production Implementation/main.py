"""Replays the naive demo's failure cases as structured model output through the real dispatcher.
The signed-in customer is u_1. No API key needed. Run: python demo_failures.py"""
import asyncio
import itertools

from anthropic.types import TextBlock, ToolUseBlock
from context import RequestContext
from tools import execute_tool_call

_ids = itertools.count(1)


def text(t: str) -> TextBlock:
    return TextBlock(type="text", text=t)


def call(name: str, **input) -> ToolUseBlock:
    return ToolUseBlock(type="tool_use", id=f"toolu_{next(_ids):02d}", name=name, input=input)


CASES = {
    "1. Conditional language fires now":
        [text("Once you've shipped the item back, I'll process REFUND: ORD-100235 $45.10 for you.")],
    "2. Negation fires anyway":
        [text("I can't do REFUND: ORD-100234 $50 because it's outside the 30-day window.")],
    "3. Thousands separator ($1,200.00)":
        [call("issue_refund", order_id="ORD-100234", amount_cents="1,200.00", reason="late")],
    "4. Sentence-ending period":
        [text("Done!"), call("issue_refund", order_id="ORD-100235", amount_cents=4510, reason="damaged")],
    "5. Markdown bold around the marker":
        [text("Let me check that."), call("get_order_status", order_id="ORD-100234")],
    "6. Near-miss syntax leaks to the customer":
        [call("issue_refund", order_id="ORD-100235", amount_cents="forty-five dollars", reason="damaged")],
    "7. Someone else's order (owned by u_2)":
        [call("get_order_status", order_id="ORD-200001")],
    "8. Two actions, one silently dropped":
        [call("get_order_status", order_id="ORD-100235"),
         call("issue_refund", order_id="ORD-100235", amount_cents=4510, reason="damaged")],
    "9. Hallucinated order ID":
        [call("issue_refund", order_id="ORD-999999", amount_cents=2000, reason="not_received")],
}


async def main() -> None:
    ctx = RequestContext(user_id="u_1", request_id="req-demo")
    for name, content in CASES.items():
        print(f"\n=== {name}")
        tool_calls = [b for b in content if b.type == "tool_use"]
        if not tool_calls:
            # No tool_use block means no side effects; prose is never parsed.
            print(f"  SENT TO CUSTOMER (nothing executed): {content[0].text!r}")
            continue
        for block in tool_calls:
            result = await execute_tool_call(block, ctx)
            status = "ERROR -> back to model" if result["is_error"] else "OK"
            print(f"  {block.name}({block.input}) -> {status}: {result['content']}")


if __name__ == "__main__":
    asyncio.run(main())
