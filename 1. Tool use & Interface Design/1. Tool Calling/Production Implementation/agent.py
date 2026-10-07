from anthropic import AsyncAnthropic
from context import RequestContext
from tools import TOOL_SCHEMAS, execute_tool_call

client = AsyncAnthropic()
MODEL = "claude-haiku-4.5"
MAX_TURNS = 8

SYSTEM = (
    "You are ShopCo's support agent. Use the provided tools to look up orders "
    "and issue refunds. Never state order details you have not retrieved (no fabrication)."
)


class AgentTurnLimitExceeded(Exception):
    pass


async def run_agent(user_message: str, ctx: RequestContext) -> str:
    messages: list[dict] = [{"role": "user", "content": user_message}]

    for _ in range(MAX_TURNS):
        resp = await client.messages.create(
            model=MODEL,
            max_tokens=1024,
            system=SYSTEM,
            tools=TOOL_SCHEMAS,
            messages=messages,
        )
        messages.append({"role": "assistant", "content": resp.content})

        if resp.stop_reason != "tool_use":
            # Final answer: only text blocks reach the customer. Streaming and yielding will be shown in future patterns
            return "".join(b.text for b in resp.content if b.type == "text")
        
        results = [
            await execute_tool_call(block, ctx)
            for block in resp.content
            if block.type == "tool_use"
        ]
        
        messages.append({"role": "user", "content": results})

    raise AgentTurnLimitExceeded()