import logging
import uuid
from collections import defaultdict
from datetime import UTC, datetime
from typing import Literal

from anthropic import AsyncAnthropic
from fastapi import FastAPI
from pydantic import BaseModel, Field
from routing import route
from schemas import TicketTriage
from settings import Settings
from triage import TriageError, triage_ticket

logging.basicConfig(level=logging.INFO)
log = logging.getLogger("triage-service")

# Change-1 : Read at import, so a bad config stops the service before it takes any traffic.
SETTINGS = Settings.from_env()


class TicketIn(BaseModel):
    subject: str = Field(min_length=1, max_length=200)
    body: str = Field(min_length=1, max_length=20_000)


class TicketOut(BaseModel):
    ticket_id: str
    status: Literal["triaged", "needs_manual_triage"]
    queue: str
    due_at: datetime
    triage: TicketTriage | None
    failure_reason: str | None = None


llmClient = AsyncAnthropic()  
# Tickets by queue name. Kept in memory here
queues: dict[str, list[TicketOut]] = defaultdict(list)

app = FastAPI(title="Ticket triage (structured output)")


@app.post("/tickets", status_code=201)
async def create_ticket(ticket: TicketIn) -> TicketOut:
    ticket_id = str(uuid.uuid4())
    triage = None
    failure_reason = None
    try:
        triage = await triage_ticket(llmClient, settings=SETTINGS, subject=ticket.subject, body=ticket.body)
    except TriageError as exc:
        log.warning("triage_failed ticket=%s reason=%s detail=%s", ticket_id, exc.reason, exc.detail)
        failure_reason = exc.reason

    queue, due_at = route(triage, now=datetime.now(UTC))
    out = TicketOut(
        ticket_id=ticket_id,
        status="triaged" if triage is not None else "needs_manual_triage",
        queue=queue,
        due_at=due_at,
        triage=triage,
        failure_reason=failure_reason,
    )
    # Every ticket is stored, including the ones the model couldn't triage.
    queues[queue].append(out)
    return out


@app.get("/queues")
async def list_queues() -> dict[str, list[TicketOut]]:
    return queues
