import json
import re
from collections import defaultdict

from anthropic import AsyncAnthropic

client = AsyncAnthropic()  # reads ANTHROPIC_API_KEY
MODEL = "claude-haiku-5-5"

SYSTEM_PROMPT = """You triage customer support tickets for ShopCo.
Respond ONLY with JSON in exactly this shape:
{"category": "billing|shipping|product|account|other",
 "priority": "P1|P2|P3|P4",
 "sentiment": "positive|neutral|negative",
 "order_ids": ["ORD-123456"],
 "requires_human": true or false,
 "summary": "one sentence"}"""

QUEUES: dict[str, list[dict]] = defaultdict(list)
SLA_HOURS = {"P1": 1, "P2": 4, "P3": 24, "P4": 72}


async def triage_ticket(subject: str, body: str) -> dict:
    resp = await client.messages.create(
        model=MODEL,
        max_tokens=300,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": f"Subject: {subject}\n\n{body}"}],
    )
    return parse_triage(resp.content[0].text) #done for simplicity sake as the triaging is providing no tools to the LLM hence expecting only a text output. Though this code would fail to run if the LLM uses thinking tokens.


def parse_triage(text: str) -> dict:
    """The 'defensive' parser most teams write: try JSON, then grab the {...} block."""
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        match = re.search(r"\{.*\}", text, re.DOTALL)
        return json.loads(match.group(0)) if match else {}


def route(subject: str, triage: dict) -> dict:
    """Defaults everywhere so it 'never crashes'."""
    priority = triage.get("priority", "P3")
    queue = "escalations" if triage.get("requires_human") else triage.get("category", "other")
    record = {
        "subject": subject,
        "queue": queue,
        "priority": priority,
        "sla_hours": SLA_HOURS.get(priority, 24),
        "order_ids": triage.get("order_ids", []),
        "summary": triage.get("summary", ""),
    }
    QUEUES[queue].append(record)
    return record