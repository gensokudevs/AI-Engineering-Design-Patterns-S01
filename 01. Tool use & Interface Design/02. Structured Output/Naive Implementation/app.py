from anthropic import AsyncAnthropic
from fastapi import FastAPI
from pydantic import BaseModel
from triage import QUEUES, route, triage_ticket

app = FastAPI(title="Ticket triage (naive)")

class TicketIn(BaseModel):
    subject: str
    body: str


@app.post("/tickets")
async def create_ticket(ticket: TicketIn):
    triage = await triage_ticket(subject=ticket.subject, body=ticket.body)
    return route(ticket.subject, triage)


@app.get("/queues")
async def list_queues():
    return QUEUES