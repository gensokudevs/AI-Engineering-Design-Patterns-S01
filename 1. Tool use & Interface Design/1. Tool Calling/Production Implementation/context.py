
from dataclasses import dataclass


@dataclass(frozen=True)
class RequestContext:
    """Identity and request metadata. Comes from auth, NEVER from model args."""
    user_id: str
    request_id: str