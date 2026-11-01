from datetime import datetime, timedelta

from schemas import Priority, TicketTriage

# How long a ticket of each priority may wait for a reply.
SLA = {
    Priority.CRITICAL: timedelta(hours=1),
    Priority.HIGH: timedelta(hours=4),
    Priority.NORMAL: timedelta(hours=24),
    Priority.LOW: timedelta(hours=72),
}
# A new priority without an SLA should break at startup, not on the first ticket that uses it.
assert set(SLA) == set(Priority), "every priority needs an SLA"


def route(triage: TicketTriage | None, now: datetime) -> tuple[str, datetime]:
    """Return the queue and due time for a ticket. The model classifies; this code decides.

    triage is None when the model's answer couldn't be used. Those tickets go to a person,
    fast, rather than to a default queue where nobody notices them.
    """
    if triage is None:
        return "manual_triage", now + SLA[Priority.HIGH]

    due_at = now + SLA[triage.priority]
    if triage.requires_human or triage.priority == Priority.CRITICAL:
        return "escalations", due_at
    return triage.category.value, due_at
